import sys
from datetime import datetime

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity


# ============================================================
# ACCESS MODELS FROM app.py
# ============================================================

main_module = sys.modules.get("__main__")

db = getattr(main_module, "db", None)
User = getattr(main_module, "User", None)
Organization = getattr(main_module, "Organization", None)
Donation = getattr(main_module, "Donation", None)
Requirement = getattr(main_module, "Requirement", None)
RequestModel = getattr(main_module, "Request", None)

# Fallback when imported separately
if db is None:
    from app import (
        db,
        User,
        Organization,
        Donation,
        Requirement,
        Request as RequestModel
    )


# ============================================================
# BLUEPRINT
# ============================================================

ngo_bp = Blueprint(
    "ngo",
    __name__,
    url_prefix="/api/ngo"
)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def get_current_user():

    user_id = get_jwt_identity()

    try:
        user_id = int(user_id)
    except (ValueError, TypeError):
        return None

    return User.query.get(user_id)


def get_ngo_organization(user):

    if not user:
        return None

    return Organization.query.filter_by(
        user_id=user.id
    ).first()


def require_ngo():

    user = get_current_user()

    if not user:
        return None, (
            jsonify({
                "message": "User not found."
            }),
            401
        )

    if user.role != "ngo":
        return None, (
            jsonify({
                "message": "Only NGO accounts can access this endpoint."
            }),
            403
        )

    organization = get_ngo_organization(user)

    if not organization:
        return None, (
            jsonify({
                "message": "NGO organization profile not found."
            }),
            404
        )

    return (user, organization), None


def organization_to_dict(organization):

    user = User.query.get(
        organization.user_id
    )

    return {
        "id": organization.id,
        "user_id": organization.user_id,

        "organization_name": organization.organization_name,
        "organization_type": organization.organization_type,
        "address": organization.address,

        "verification_status": organization.verification_status,

        "is_verified": (
            organization.verification_status == "approved"
        ),

        "email": user.email if user else None,
        "phone": user.phone if user else None,

        "created_at": (
            organization.created_at.isoformat()
            if organization.created_at
            else None
        )
    }


def requirement_to_dict(requirement):

    organization = Organization.query.get(
        requirement.organization_id
    )

    return {
        "id": requirement.id,

        "organization_id": requirement.organization_id,

        "organization_name": (
            organization.organization_name
            if organization
            else "NGO"
        ),

        "category": requirement.category,
        "item_name": requirement.item_name,
        "quantity_required": requirement.quantity_required,
        "priority": requirement.priority,
        "description": requirement.description,
        "location": requirement.location,
        "status": requirement.status,

        "created_at": (
            requirement.created_at.isoformat()
            if requirement.created_at
            else None
        )
    }


def donation_to_dict(donation):

    donor = User.query.get(
        donation.donor_id
    )

    return {
        "id": donation.id,
        "donation_id": donation.id,

        "category": donation.category,
        "item_name": donation.item_name,
        "quantity": donation.quantity,
        "condition": donation.condition,

        "description": donation.description,
        "location": donation.location,

        "donation_type": donation.donation_type,
        "target_type": donation.target_type,

        "status": donation.status,

        "donor_id": donation.donor_id,
        "donor_name": (
            donor.name
            if donor
            else "Donor"
        ),
        "donor_phone": (
            donor.phone
            if donor
            else ""
        ),

        "created_at": (
            donation.created_at.isoformat()
            if donation.created_at
            else None
        )
    }


def request_to_dict(request_obj):

    donation = None

    if request_obj.donation_id:
        donation = Donation.query.get(
            request_obj.donation_id
        )

    requester = User.query.get(
        request_obj.requester_id
    )

    return {
        "id": request_obj.id,

        "donation_id": request_obj.donation_id,

        "requester_id": request_obj.requester_id,

        "requester_name": (
            requester.name
            if requester
            else None
        ),

        "status": request_obj.status,

        "donation": (
            donation_to_dict(donation)
            if donation
            else None
        ),

        "created_at": (
            request_obj.created_at.isoformat()
            if request_obj.created_at
            else None
        )
    }


# ============================================================
# NGO PROFILE
# ============================================================

@ngo_bp.route("/profile", methods=["GET"])
@jwt_required()
def get_profile():

    result, error = require_ngo()

    if error:
        return error

    user, organization = result

    return jsonify({

        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "phone": user.phone,
            "role": user.role,
            "is_verified": user.is_verified
        },

        "organization": organization_to_dict(
            organization
        )

    }), 200


# ============================================================
# NGO DASHBOARD
# ============================================================

@ngo_bp.route("/dashboard", methods=["GET"])
@jwt_required()
def dashboard():

    result, error = require_ngo()

    if error:
        return error

    user, organization = result

    total_requirements = Requirement.query.filter_by(
        organization_id=organization.id
    ).count()

    active_requirements = Requirement.query.filter_by(
        organization_id=organization.id,
        status="active"
    ).count()

    fulfilled_requirements = Requirement.query.filter_by(
        organization_id=organization.id,
        status="fulfilled"
    ).count()

    incoming_requests = RequestModel.query.filter_by(
        organization_id=organization.id
    ).count()

    return jsonify({

        "organization": organization_to_dict(
            organization
        ),

        "stats": {
            "total_requirements": total_requirements,
            "active_requirements": active_requirements,
            "fulfilled_requirements": fulfilled_requirements,
            "incoming_requests": incoming_requests
        }

    }), 200


# ============================================================
# GET NGO REQUIREMENTS
# ============================================================

@ngo_bp.route("/requirements", methods=["GET"])
@jwt_required()
def get_requirements():

    result, error = require_ngo()

    if error:
        return error

    user, organization = result

    requirements = Requirement.query.filter_by(
        organization_id=organization.id
    ).order_by(
        Requirement.created_at.desc()
    ).all()

    return jsonify([
        requirement_to_dict(requirement)
        for requirement in requirements
    ]), 200


# ============================================================
# CREATE REQUIREMENT
# ============================================================

@ngo_bp.route("/requirements", methods=["POST"])
@jwt_required()
def create_requirement():

    result, error = require_ngo()

    if error:
        return error

    user, organization = result

    data = request.get_json() or {}

    category = str(
        data.get("category", "")
    ).strip()

    item_name = str(
        data.get("item_name", "")
    ).strip()

    description = str(
        data.get("description", "")
    ).strip()

    location = str(
        data.get("location")
        or organization.address
        or user.location
        or ""
    ).strip()

    priority = str(
        data.get("priority", "medium")
    ).strip().lower()

    quantity_required = data.get(
        "quantity_required"
    )

    # --------------------------------------------------------
    # Validation
    # --------------------------------------------------------

    if not category:
        return jsonify({
            "message": "Category is required."
        }), 400

    if not item_name:
        return jsonify({
            "message": "Item name is required."
        }), 400

    if quantity_required is None:
        return jsonify({
            "message": "Quantity is required."
        }), 400

    try:
        quantity_required = int(
            quantity_required
        )
    except (ValueError, TypeError):

        return jsonify({
            "message": "Quantity must be a number."
        }), 400

    if quantity_required <= 0:
        return jsonify({
            "message": "Quantity must be greater than zero."
        }), 400

    if priority not in [
        "low",
        "medium",
        "high",
        "urgent"
    ]:
        priority = "medium"

    # --------------------------------------------------------
    # Create requirement
    # --------------------------------------------------------

    requirement = Requirement(
        organization_id=organization.id,

        category=category,

        item_name=item_name,

        quantity_required=quantity_required,

        priority=priority,

        description=description,

        location=location,

        status="active"
    )

    db.session.add(
        requirement
    )

    try:

        db.session.commit()

        return jsonify({
            "message": "Requirement posted successfully.",
            "requirement": requirement_to_dict(
                requirement
            )
        }), 201

    except Exception as error:

        db.session.rollback()

        return jsonify({
            "message": "Could not create requirement.",
            "error": str(error)
        }), 500


# ============================================================
# CLOSE REQUIREMENT
# ============================================================

@ngo_bp.route(
    "/requirements/<int:requirement_id>/close",
    methods=["POST"]
)
@jwt_required()
def close_requirement(requirement_id):

    result, error = require_ngo()

    if error:
        return error

    user, organization = result

    requirement = Requirement.query.filter_by(
        id=requirement_id,
        organization_id=organization.id
    ).first()

    if not requirement:

        return jsonify({
            "message": "Requirement not found."
        }), 404

    requirement.status = "closed"

    try:

        db.session.commit()

        return jsonify({
            "message": "Requirement closed successfully.",
            "requirement": requirement_to_dict(
                requirement
            )
        }), 200

    except Exception as error:

        db.session.rollback()

        return jsonify({
            "message": "Could not close requirement.",
            "error": str(error)
        }), 500


# ============================================================
# FULFILL REQUIREMENT
# ============================================================

@ngo_bp.route(
    "/requirements/<int:requirement_id>/fulfill",
    methods=["POST"]
)
@jwt_required()
def fulfill_requirement(requirement_id):

    result, error = require_ngo()

    if error:
        return error

    user, organization = result

    requirement = Requirement.query.filter_by(
        id=requirement_id,
        organization_id=organization.id
    ).first()

    if not requirement:

        return jsonify({
            "message": "Requirement not found."
        }), 404

    requirement.status = "fulfilled"

    try:

        db.session.commit()

        return jsonify({
            "message": "Requirement marked as fulfilled.",
            "requirement": requirement_to_dict(
                requirement
            )
        }), 200

    except Exception as error:

        db.session.rollback()

        return jsonify({
            "message": "Could not update requirement.",
            "error": str(error)
        }), 500


# ============================================================
# FIND MATCHING DONATIONS
# ============================================================

@ngo_bp.route("/donations/matches", methods=["GET"])
@jwt_required()
def matching_donations():

    result, error = require_ngo()

    if error:
        return error

    user, organization = result

    requirements = Requirement.query.filter_by(
        organization_id=organization.id,
        status="active"
    ).all()

    if not requirements:

        return jsonify([]), 200

    donations = Donation.query.filter_by(
        status="available"
    ).order_by(
        Donation.created_at.desc()
    ).all()

    matches = []

    for donation in donations:

        for requirement in requirements:

            category_match = (
                donation.category.lower()
                == requirement.category.lower()
            )

            item_match = (
                donation.item_name.lower()
                == requirement.item_name.lower()
            )

            # Match either exact category or exact item.
            if category_match or item_match:

                match_score = 0

                if category_match:
                    match_score += 50

                if item_match:
                    match_score += 50

                if (
                    donation.location
                    and requirement.location
                    and donation.location.lower()
                    == requirement.location.lower()
                ):
                    match_score += 25

                matches.append({

                    "match_score": match_score,

                    "requirement": (
                        requirement_to_dict(
                            requirement
                        )
                    ),

                    "donation": (
                        donation_to_dict(
                            donation
                        )
                    )

                })

                break

    matches.sort(
        key=lambda item: item["match_score"],
        reverse=True
    )

    return jsonify(matches), 200


# ============================================================
# NGO REQUESTS
# ============================================================

@ngo_bp.route("/requests", methods=["GET"])
@jwt_required()
def get_requests():

    result, error = require_ngo()

    if error:
        return error

    user, organization = result

    requests_list = RequestModel.query.filter_by(
        organization_id=organization.id
    ).order_by(
        RequestModel.created_at.desc()
    ).all()

    return jsonify([
        request_to_dict(request_obj)
        for request_obj in requests_list
    ]), 200


# ============================================================
# REQUEST A DONATION
# ============================================================

@ngo_bp.route(
    "/donations/<int:donation_id>/request",
    methods=["POST"]
)
@jwt_required()
def request_donation(donation_id):

    result, error = require_ngo()

    if error:
        return error

    user, organization = result

    donation = Donation.query.get(
        donation_id
    )

    if not donation:

        return jsonify({
            "message": "Donation not found."
        }), 404

    if donation.status != "available":

        return jsonify({
            "message": "This donation is no longer available."
        }), 409

    # --------------------------------------------------------
    # Check duplicate request
    # --------------------------------------------------------

    existing = RequestModel.query.filter_by(
        donation_id=donation.id,
        organization_id=organization.id
    ).first()

    if existing:

        return jsonify({
            "message": "Your organization has already requested this donation.",
            "request": request_to_dict(existing)
        }), 409

    # --------------------------------------------------------
    # Create request
    # --------------------------------------------------------

    request_obj = RequestModel(
        donation_id=donation.id,

        requester_id=user.id,

        organization_id=organization.id,

        status="pending"
    )

    db.session.add(
        request_obj
    )

    try:

        db.session.commit()

        return jsonify({
            "message": "Donation request sent successfully.",
            "request": request_to_dict(
                request_obj
            )
        }), 201

    except Exception as error:

        db.session.rollback()

        return jsonify({
            "message": "Could not send donation request.",
            "error": str(error)
        }), 500


# ============================================================
# ACCEPT DONATION REQUEST
# ============================================================

@ngo_bp.route(
    "/requests/<int:request_id>/accept",
    methods=["POST"]
)
@jwt_required()
def accept_request(request_id):

    result, error = require_ngo()

    if error:
        return error

    user, organization = result

    request_obj = RequestModel.query.filter_by(
        id=request_id,
        organization_id=organization.id
    ).first()

    if not request_obj:

        return jsonify({
            "message": "Request not found."
        }), 404

    if request_obj.status not in [
        "pending",
        "requested"
    ]:

        return jsonify({
            "message": "This request cannot be accepted."
        }), 400

    donation = None

    if request_obj.donation_id:

        donation = Donation.query.get(
            request_obj.donation_id
        )

    if donation:

        if donation.status not in [
            "available",
            "requested"
        ]:

            return jsonify({
                "message": "This donation is no longer available."
            }), 409

        donation.status = "requested"

    request_obj.status = "accepted"

    try:

        db.session.commit()

        return jsonify({
            "message": "Donation request accepted.",
            "request": request_to_dict(
                request_obj
            )
        }), 200

    except Exception as error:

        db.session.rollback()

        return jsonify({
            "message": "Could not accept request.",
            "error": str(error)
        }), 500


# ============================================================
# REJECT DONATION REQUEST
# ============================================================

@ngo_bp.route(
    "/requests/<int:request_id>/reject",
    methods=["POST"]
)
@jwt_required()
def reject_request(request_id):

    result, error = require_ngo()

    if error:
        return error

    user, organization = result

    request_obj = RequestModel.query.filter_by(
        id=request_id,
        organization_id=organization.id
    ).first()

    if not request_obj:

        return jsonify({
            "message": "Request not found."
        }), 404

    request_obj.status = "rejected"

    try:

        db.session.commit()

        return jsonify({
            "message": "Donation request rejected.",
            "request": request_to_dict(
                request_obj
            )
        }), 200

    except Exception as error:

        db.session.rollback()

        return jsonify({
            "message": "Could not reject request.",
            "error": str(error)
        }), 500


# ============================================================
# REGISTER BLUEPRINT
# ============================================================

def register_ngo_routes(app):

    app.register_blueprint(
        ngo_bp
    )

    with app.app_context():
        db.create_all()