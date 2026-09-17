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
BloodInventory = getattr(main_module, "BloodInventory", None)
BloodRequest = getattr(main_module, "BloodRequest", None)

if db is None:
    from app import (
        db,
        User,
        Organization,
        BloodInventory,
        BloodRequest
    )


# ============================================================
# BLUEPRINT
# ============================================================

blood_bp = Blueprint(
    "blood",
    __name__,
    url_prefix="/api/blood"
)


# ============================================================
# HELPERS
# ============================================================

VALID_BLOOD_GROUPS = [
    "A+",
    "A-",
    "B+",
    "B-",
    "AB+",
    "AB-",
    "O+",
    "O-"
]


def get_current_user():

    user_id = get_jwt_identity()

    try:
        user_id = int(user_id)
    except (ValueError, TypeError):
        return None

    return User.query.get(user_id)


def get_blood_bank(user):

    if not user:
        return None

    return Organization.query.filter_by(
        user_id=user.id
    ).first()


def require_blood_bank():

    user = get_current_user()

    if not user:
        return None, (
            jsonify({
                "message": "User not found."
            }),
            401
        )

    if user.role != "blood_bank":
        return None, (
            jsonify({
                "message": "Only blood bank accounts can access this endpoint."
            }),
            403
        )

    organization = get_blood_bank(user)

    if not organization:
        return None, (
            jsonify({
                "message": "Blood bank organization profile not found."
            }),
            404
        )

    return (user, organization), None


def inventory_to_dict(item):

    organization = Organization.query.get(
        item.organization_id
    )

    return {
        "id": item.id,

        "organization_id": item.organization_id,

        "organization_name": (
            organization.organization_name
            if organization
            else "Blood Bank"
        ),

        "blood_group": item.blood_group,

        "units_available": item.units_available,

        "units": item.units_available,

        "last_updated": (
            item.last_updated.isoformat()
            if item.last_updated
            else None
        )
    }


def blood_request_to_dict(item):

    organization = Organization.query.get(
        item.organization_id
    )

    return {
        "id": item.id,

        "organization_id": item.organization_id,

        "organization_name": (
            organization.organization_name
            if organization
            else "Blood Bank"
        ),

        "blood_group": item.blood_group,

        "units_required": item.units_required,

        "units": item.units_required,

        "urgency": item.urgency,

        "hospital_name": item.hospital_name,

        "patient_reference": item.patient_reference,

        "contact": item.contact,

        "status": item.status,

        "created_at": (
            item.created_at.isoformat()
            if item.created_at
            else None
        )
    }


# ============================================================
# BLOOD BANK PROFILE
# ============================================================

@blood_bp.route("/profile", methods=["GET"])
@jwt_required()
def profile():

    result, error = require_blood_bank()

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

        "organization": {
            "id": organization.id,
            "organization_name": organization.organization_name,
            "organization_type": organization.organization_type,
            "address": organization.address,
            "verification_status": organization.verification_status,
            "is_verified": (
                organization.verification_status == "approved"
            )
        }

    }), 200


# ============================================================
# DASHBOARD
# ============================================================

@blood_bp.route("/dashboard", methods=["GET"])
@jwt_required()
def dashboard():

    result, error = require_blood_bank()

    if error:
        return error

    user, organization = result

    inventory = BloodInventory.query.filter_by(
        organization_id=organization.id
    ).all()

    requests = BloodRequest.query.filter_by(
        organization_id=organization.id
    ).all()

    total_units = sum(
        item.units_available
        for item in inventory
    )

    active_requests = sum(
        1
        for item in requests
        if item.status == "active"
    )

    return jsonify({

        "stats": {
            "blood_groups": len(inventory),
            "total_units": total_units,
            "active_requests": active_requests,
            "total_requests": len(requests)
        },

        "inventory": [
            inventory_to_dict(item)
            for item in inventory
        ]

    }), 200


# ============================================================
# GET INVENTORY
# ============================================================

@blood_bp.route("/inventory", methods=["GET"])
@jwt_required()
def get_inventory():

    result, error = require_blood_bank()

    if error:
        return error

    user, organization = result

    inventory = BloodInventory.query.filter_by(
        organization_id=organization.id
    ).order_by(
        BloodInventory.blood_group.asc()
    ).all()

    return jsonify([
        inventory_to_dict(item)
        for item in inventory
    ]), 200


# ============================================================
# ADD / UPDATE INVENTORY
# ============================================================

@blood_bp.route("/inventory", methods=["POST"])
@jwt_required()
def add_inventory():

    result, error = require_blood_bank()

    if error:
        return error

    user, organization = result

    data = request.get_json() or {}

    blood_group = str(
        data.get("blood_group", "")
    ).strip().upper()

    units = data.get("units")

    if blood_group not in VALID_BLOOD_GROUPS:

        return jsonify({
            "message": "Invalid blood group.",
            "valid_groups": VALID_BLOOD_GROUPS
        }), 400

    if units is None:

        return jsonify({
            "message": "Units are required."
        }), 400

    try:

        units = int(units)

    except (ValueError, TypeError):

        return jsonify({
            "message": "Units must be a number."
        }), 400

    if units < 0:

        return jsonify({
            "message": "Units cannot be negative."
        }), 400

    inventory = BloodInventory.query.filter_by(
        organization_id=organization.id,
        blood_group=blood_group
    ).first()

    if inventory:

        inventory.units_available = units

    else:

        inventory = BloodInventory(
            organization_id=organization.id,
            blood_group=blood_group,
            units_available=units
        )

        db.session.add(inventory)

    try:

        db.session.commit()

        return jsonify({
            "message": "Blood inventory updated successfully.",
            "inventory": inventory_to_dict(
                inventory
            )
        }), 200

    except Exception as error:

        db.session.rollback()

        return jsonify({
            "message": "Could not update inventory.",
            "error": str(error)
        }), 500


# ============================================================
# GET BLOOD REQUESTS
# ============================================================

@blood_bp.route("/requests", methods=["GET"])
@jwt_required()
def get_requests():

    result, error = require_blood_bank()

    if error:
        return error

    user, organization = result

    requests_list = BloodRequest.query.filter_by(
        organization_id=organization.id
    ).order_by(
        BloodRequest.created_at.desc()
    ).all()

    return jsonify([
        blood_request_to_dict(item)
        for item in requests_list
    ]), 200


# ============================================================
# CREATE BLOOD REQUEST
# ============================================================

@blood_bp.route("/requests", methods=["POST"])
@jwt_required()
def create_request():

    result, error = require_blood_bank()

    if error:
        return error

    user, organization = result

    data = request.get_json() or {}

    blood_group = str(
        data.get("blood_group", "")
    ).strip().upper()

    units_required = data.get(
        "units_required"
    )

    urgency = str(
        data.get("urgency", "normal")
    ).strip().lower()

    hospital_name = str(
        data.get("hospital_name", "")
    ).strip()

    patient_reference = str(
        data.get("patient_reference", "")
    ).strip()

    contact = str(
        data.get("contact")
        or user.phone
        or ""
    ).strip()

    if blood_group not in VALID_BLOOD_GROUPS:

        return jsonify({
            "message": "Invalid blood group."
        }), 400

    if units_required is None:

        return jsonify({
            "message": "Required units are missing."
        }), 400

    try:

        units_required = int(
            units_required
        )

    except (ValueError, TypeError):

        return jsonify({
            "message": "Required units must be a number."
        }), 400

    if units_required <= 0:

        return jsonify({
            "message": "Required units must be greater than zero."
        }), 400

    if urgency not in [
        "normal",
        "high",
        "urgent",
        "critical"
    ]:
        urgency = "normal"

    blood_request = BloodRequest(

        organization_id=organization.id,

        blood_group=blood_group,

        units_required=units_required,

        urgency=urgency,

        hospital_name=hospital_name,

        patient_reference=patient_reference,

        contact=contact,

        status="active"
    )

    db.session.add(
        blood_request
    )

    try:

        db.session.commit()

        return jsonify({
            "message": "Blood request created successfully.",
            "request": blood_request_to_dict(
                blood_request
            )
        }), 201

    except Exception as error:

        db.session.rollback()

        return jsonify({
            "message": "Could not create blood request.",
            "error": str(error)
        }), 500


# ============================================================
# CLOSE BLOOD REQUEST
# ============================================================

@blood_bp.route(
    "/requests/<int:request_id>/close",
    methods=["POST"]
)
@jwt_required()
def close_request(request_id):

    result, error = require_blood_bank()

    if error:
        return error

    user, organization = result

    blood_request = BloodRequest.query.filter_by(
        id=request_id,
        organization_id=organization.id
    ).first()

    if not blood_request:

        return jsonify({
            "message": "Blood request not found."
        }), 404

    blood_request.status = "closed"

    try:

        db.session.commit()

        return jsonify({
            "message": "Blood request closed successfully.",
            "request": blood_request_to_dict(
                blood_request
            )
        }), 200

    except Exception as error:

        db.session.rollback()

        return jsonify({
            "message": "Could not close blood request.",
            "error": str(error)
        }), 500


# ============================================================
# REGISTER ROUTES
# ============================================================

def register_blood_routes(app):

    app.register_blueprint(
        blood_bp
    )

    with app.app_context():
        db.create_all()