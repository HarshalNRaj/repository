import os
import sys
from datetime import datetime

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename


# ============================================================
# ACCESS MODELS FROM app.py
# ============================================================

main_module = sys.modules.get("__main__")

db = getattr(main_module, "db", None)
User = getattr(main_module, "User", None)
Donation = getattr(main_module, "Donation", None)
RequestModel = getattr(main_module, "Request", None)
VolunteerTask = getattr(main_module, "VolunteerTask", None)

# Fallback when this file is imported separately
if db is None:
    from app import db, User, Donation, Request as RequestModel, VolunteerTask


# ============================================================
# BLUEPRINT
# ============================================================

volunteer_bp = Blueprint(
    "volunteer",
    __name__,
    url_prefix="/api/volunteer"
)


# ============================================================
# VOLUNTEER PROFILE MODEL
# ============================================================

class VolunteerProfile(db.Model):
    __tablename__ = "volunteer_profiles"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
        unique=True
    )

    service_area = db.Column(db.String(200), nullable=False)
    skills = db.Column(db.String(500), nullable=True)
    availability = db.Column(db.String(100), nullable=True)
    document = db.Column(db.String(300), nullable=True)

    verification_status = db.Column(
        db.String(50),
        default="verified"
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def get_current_user():
    """
    Get the currently logged-in user from JWT.
    """

    user_id = get_jwt_identity()

    try:
        user_id = int(user_id)
    except (ValueError, TypeError):
        return None

    return User.query.get(user_id)


def user_is_volunteer(user):
    return user and user.role == "volunteer"


def donation_to_dict(donation):
    """
    Convert Donation object into JSON-friendly data.
    """

    donor = User.query.get(donation.donor_id)

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
        "donor_name": donor.name if donor else "Unknown",
        "donor_phone": donor.phone if donor else "",
        "donor_location": donor.location if donor else donation.location,
        "created_at": (
            donation.created_at.isoformat()
            if donation.created_at
            else None
        ),
    }


def task_to_dict(task):
    """
    Convert VolunteerTask into JSON-friendly data.
    """

    request_obj = RequestModel.query.get(task.request_id)

    donation = None

    if request_obj and request_obj.donation_id:
        donation = Donation.query.get(request_obj.donation_id)

    volunteer = User.query.get(task.volunteer_id)

    donor = None

    if donation:
        donor = User.query.get(donation.donor_id)

    receiver = None

    if request_obj:
        receiver = User.query.get(request_obj.requester_id)

    return {
        "id": task.id,
        "task_id": task.id,

        "request_id": task.request_id,

        "donation_id": (
            donation.id
            if donation
            else None
        ),

        "status": task.status,

        "pickup_location": task.pickup_location,
        "delivery_location": task.delivery_location,

        "volunteer_id": task.volunteer_id,
        "volunteer_name": (
            volunteer.name
            if volunteer
            else None
        ),

        "item_name": (
            donation.item_name
            if donation
            else "Donation"
        ),

        "category": (
            donation.category
            if donation
            else None
        ),

        "quantity": (
            donation.quantity
            if donation
            else None
        ),

        "condition": (
            donation.condition
            if donation
            else None
        ),

        "description": (
            donation.description
            if donation
            else None
        ),

        "donor_id": (
            donation.donor_id
            if donation
            else None
        ),

        "donor_name": (
            donor.name
            if donor
            else None
        ),

        "donor_phone": (
            donor.phone
            if donor
            else None
        ),

        "donor_location": (
            donor.location
            if donor
            else None
        ),

        "receiver_id": (
            request_obj.requester_id
            if request_obj
            else None
        ),

        "receiver_name": (
            receiver.name
            if receiver
            else None
        ),

        "receiver_phone": (
            receiver.phone
            if receiver
            else None
        ),

        "receiver_location": (
            receiver.location
            if receiver
            else None
        ),

        "created_at": (
            task.created_at.isoformat()
            if task.created_at
            else None
        ),
    }


# ============================================================
# VOLUNTEER PROFILE / VERIFICATION
# ============================================================

@volunteer_bp.route("/verify", methods=["POST"])
@jwt_required()
def verify_volunteer():

    user = get_current_user()

    if not user_is_volunteer(user):
        return jsonify({
            "message": "Only volunteer accounts can access this endpoint."
        }), 403

    service_area = request.form.get(
        "service_area",
        ""
    ).strip()

    skills = request.form.get(
        "skills",
        ""
    ).strip()

    availability = request.form.get(
        "availability",
        ""
    ).strip()

    phone = request.form.get(
        "phone",
        ""
    ).strip()

    document = request.files.get("document")

    if not service_area:
        return jsonify({
            "message": "Service area is required."
        }), 400

    if not skills:
        return jsonify({
            "message": "Skills are required."
        }), 400

    if not availability:
        return jsonify({
            "message": "Availability is required."
        }), 400

    # --------------------------------------------------------
    # Save document if supplied
    # --------------------------------------------------------

    document_filename = None

    if document and document.filename:

        upload_folder = os.path.join(
            os.path.dirname(__file__),
            "uploads",
            "volunteer_documents"
        )

        os.makedirs(
            upload_folder,
            exist_ok=True
        )

        document_filename = secure_filename(
            document.filename
        )

        document_path = os.path.join(
            upload_folder,
            document_filename
        )

        document.save(document_path)

    # --------------------------------------------------------
    # Find existing profile
    # --------------------------------------------------------

    profile = VolunteerProfile.query.filter_by(
        user_id=user.id
    ).first()

    if profile is None:

        profile = VolunteerProfile(
            user_id=user.id
        )

        db.session.add(profile)

    profile.service_area = service_area
    profile.skills = skills
    profile.availability = availability

    if document_filename:
        profile.document = document_filename

    # --------------------------------------------------------
    # DEMO VERIFICATION
    # --------------------------------------------------------
    # For the college demonstration, volunteer verification
    # is completed automatically after submitting the form.
    #
    # In a production system this should be reviewed by admin.
    # --------------------------------------------------------

    profile.verification_status = "verified"

    user.is_verified = True

    if phone:
        user.phone = phone

    user.location = service_area

    try:

        db.session.commit()

        return jsonify({
            "message": "Volunteer profile verified successfully.",
            "status": "verified",
            "profile": {
                "id": profile.id,
                "user_id": profile.user_id,
                "service_area": profile.service_area,
                "skills": profile.skills,
                "availability": profile.availability,
                "verification_status": profile.verification_status
            }
        }), 200

    except Exception as error:

        db.session.rollback()

        return jsonify({
            "message": "Could not save volunteer profile.",
            "error": str(error)
        }), 500


# ============================================================
# GET VOLUNTEER PROFILE
# ============================================================

@volunteer_bp.route("/profile", methods=["GET"])
@jwt_required()
def get_volunteer_profile():

    user = get_current_user()

    if not user_is_volunteer(user):
        return jsonify({
            "message": "Only volunteers can access this endpoint."
        }), 403

    profile = VolunteerProfile.query.filter_by(
        user_id=user.id
    ).first()

    return jsonify({

        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "phone": user.phone,
            "location": user.location,
            "role": user.role,
            "is_verified": user.is_verified
        },

        "profile": (
            {
                "id": profile.id,
                "service_area": profile.service_area,
                "skills": profile.skills,
                "availability": profile.availability,
                "document": profile.document,
                "verification_status": profile.verification_status
            }
            if profile
            else None
        )

    }), 200


# ============================================================
# VOLUNTEER DASHBOARD
# ============================================================

@volunteer_bp.route("/dashboard", methods=["GET"])
@jwt_required()
def volunteer_dashboard():

    user = get_current_user()

    if not user_is_volunteer(user):
        return jsonify({
            "message": "Only volunteers can access this endpoint."
        }), 403

    total_tasks = VolunteerTask.query.filter_by(
        volunteer_id=user.id
    ).count()

    completed_tasks = VolunteerTask.query.filter_by(
        volunteer_id=user.id,
        status="completed"
    ).count()

    ongoing_tasks = VolunteerTask.query.filter(
        VolunteerTask.volunteer_id == user.id,
        VolunteerTask.status.in_([
            "accepted",
            "picked_up",
            "delivered"
        ])
    ).count()

    available_donations = Donation.query.filter_by(
        status="available"
    ).count()

    return jsonify({

        "stats": {
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "ongoing_tasks": ongoing_tasks,
            "available_donations": available_donations
        }

    }), 200


# ============================================================
# AVAILABLE DONATIONS
# ============================================================

@volunteer_bp.route("/tasks/available", methods=["GET"])
@jwt_required()
def available_tasks():

    user = get_current_user()

    if not user_is_volunteer(user):
        return jsonify({
            "message": "Only volunteers can access this endpoint."
        }), 403

    donations = Donation.query.filter(
        Donation.status == "available",
        Donation.donor_id != user.id
    ).order_by(
        Donation.created_at.desc()
    ).all()

    return jsonify([
        donation_to_dict(donation)
        for donation in donations
    ]), 200


# ============================================================
# CREATE / ACCEPT VOLUNTEER TASK
# ============================================================

@volunteer_bp.route("/tasks/create", methods=["POST"])
@jwt_required()
def create_task():

    user = get_current_user()

    if not user_is_volunteer(user):
        return jsonify({
            "message": "Only volunteers can create tasks."
        }), 403

    data = request.get_json() or {}

    donation_id = data.get("donation_id")

    pickup_location = (
        data.get("pickup_location")
        or ""
    ).strip()

    delivery_location = (
        data.get("delivery_location")
        or ""
    ).strip()

    if not donation_id:
        return jsonify({
            "message": "Donation ID is required."
        }), 400

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

    if donation.donor_id == user.id:
        return jsonify({
            "message": "You cannot volunteer for your own donation."
        }), 400

    # --------------------------------------------------------
    # Check if another task already exists
    # --------------------------------------------------------

    existing_request = RequestModel.query.filter_by(
        donation_id=donation.id
    ).filter(
        RequestModel.status.in_([
            "accepted",
            "pickup",
            "picked_up",
            "delivered"
        ])
    ).first()

    if existing_request:

        existing_task = VolunteerTask.query.filter_by(
            request_id=existing_request.id
        ).first()

        if existing_task:
            return jsonify({
                "message": "This donation already has a volunteer task."
            }), 409

    # --------------------------------------------------------
    # Create request
    # --------------------------------------------------------

    request_obj = RequestModel(
        donation_id=donation.id,
        requester_id=user.id,
        status="accepted"
    )

    db.session.add(request_obj)

    db.session.flush()

    # --------------------------------------------------------
    # Create volunteer task
    # --------------------------------------------------------

    task = VolunteerTask(
        volunteer_id=user.id,
        request_id=request_obj.id,
        pickup_location=(
            pickup_location
            or donation.location
            or user.location
            or "Pickup location not specified"
        ),
        delivery_location=(
            delivery_location
            or "Receiver / organization location"
        ),
        status="accepted"
    )

    db.session.add(task)

    # --------------------------------------------------------
    # Update donation
    # --------------------------------------------------------

    donation.status = "requested"

    try:

        db.session.commit()

        return jsonify({
            "message": "Volunteer task accepted successfully.",
            "task": task_to_dict(task)
        }), 201

    except Exception as error:

        db.session.rollback()

        return jsonify({
            "message": "Could not create volunteer task.",
            "error": str(error)
        }), 500


# ============================================================
# MY TASKS
# ============================================================

@volunteer_bp.route("/tasks/my", methods=["GET"])
@jwt_required()
def my_tasks():

    user = get_current_user()

    if not user_is_volunteer(user):
        return jsonify({
            "message": "Only volunteers can access this endpoint."
        }), 403

    tasks = VolunteerTask.query.filter_by(
        volunteer_id=user.id
    ).order_by(
        VolunteerTask.created_at.desc()
    ).all()

    return jsonify([
        task_to_dict(task)
        for task in tasks
    ]), 200


# ============================================================
# ACCEPT TASK
# ============================================================

@volunteer_bp.route(
    "/tasks/<int:task_id>/accept",
    methods=["POST"]
)
@jwt_required()
def accept_task(task_id):

    user = get_current_user()

    if not user_is_volunteer(user):
        return jsonify({
            "message": "Only volunteers can accept tasks."
        }), 403

    task = VolunteerTask.query.get(
        task_id
    )

    if not task:
        return jsonify({
            "message": "Task not found."
        }), 404

    if task.volunteer_id != user.id:
        return jsonify({
            "message": "You are not assigned to this task."
        }), 403

    request_obj = RequestModel.query.get(
        task.request_id
    )

    if request_obj:
        request_obj.status = "accepted"

        if request_obj.donation_id:

            donation = Donation.query.get(
                request_obj.donation_id
            )

            if donation:
                donation.status = "requested"

    task.status = "accepted"

    try:

        db.session.commit()

        return jsonify({
            "message": "Task accepted.",
            "task": task_to_dict(task)
        }), 200

    except Exception as error:

        db.session.rollback()

        return jsonify({
            "message": "Could not accept task.",
            "error": str(error)
        }), 500


# ============================================================
# PICKUP
# ============================================================

@volunteer_bp.route(
    "/tasks/<int:task_id>/pickup",
    methods=["POST"]
)
@jwt_required()
def pickup_task(task_id):

    user = get_current_user()

    if not user_is_volunteer(user):
        return jsonify({
            "message": "Only volunteers can update tasks."
        }), 403

    task = VolunteerTask.query.get(
        task_id
    )

    if not task:
        return jsonify({
            "message": "Task not found."
        }), 404

    if task.volunteer_id != user.id:
        return jsonify({
            "message": "You are not assigned to this task."
        }), 403

    task.status = "picked_up"

    request_obj = RequestModel.query.get(
        task.request_id
    )

    if request_obj:
        request_obj.status = "picked_up"

        if request_obj.donation_id:

            donation = Donation.query.get(
                request_obj.donation_id
            )

            if donation:
                donation.status = "pickup"

    try:

        db.session.commit()

        return jsonify({
            "message": "Donation marked as picked up.",
            "task": task_to_dict(task)
        }), 200

    except Exception as error:

        db.session.rollback()

        return jsonify({
            "message": "Could not update pickup status.",
            "error": str(error)
        }), 500


# ============================================================
# DELIVERY
# ============================================================

@volunteer_bp.route(
    "/tasks/<int:task_id>/deliver",
    methods=["POST"]
)
@jwt_required()
def deliver_task(task_id):

    user = get_current_user()

    if not user_is_volunteer(user):
        return jsonify({
            "message": "Only volunteers can update tasks."
        }), 403

    task = VolunteerTask.query.get(
        task_id
    )

    if not task:
        return jsonify({
            "message": "Task not found."
        }), 404

    if task.volunteer_id != user.id:
        return jsonify({
            "message": "You are not assigned to this task."
        }), 403

    task.status = "delivered"

    request_obj = RequestModel.query.get(
        task.request_id
    )

    if request_obj:
        request_obj.status = "delivered"

        if request_obj.donation_id:

            donation = Donation.query.get(
                request_obj.donation_id
            )

            if donation:
                donation.status = "delivered"

    try:

        db.session.commit()

        return jsonify({
            "message": "Donation marked as delivered.",
            "task": task_to_dict(task)
        }), 200

    except Exception as error:

        db.session.rollback()

        return jsonify({
            "message": "Could not update delivery status.",
            "error": str(error)
        }), 500


# ============================================================
# COMPLETE TASK
# ============================================================

@volunteer_bp.route(
    "/tasks/<int:task_id>/complete",
    methods=["POST"]
)
@jwt_required()
def complete_task(task_id):

    user = get_current_user()

    if not user_is_volunteer(user):
        return jsonify({
            "message": "Only volunteers can update tasks."
        }), 403

    task = VolunteerTask.query.get(
        task_id
    )

    if not task:
        return jsonify({
            "message": "Task not found."
        }), 404

    if task.volunteer_id != user.id:
        return jsonify({
            "message": "You are not assigned to this task."
        }), 403

    task.status = "completed"

    request_obj = RequestModel.query.get(
        task.request_id
    )

    if request_obj:
        request_obj.status = "completed"

        if request_obj.donation_id:

            donation = Donation.query.get(
                request_obj.donation_id
            )

            if donation:
                donation.status = "completed"

    try:

        db.session.commit()

        return jsonify({
            "message": "Task completed successfully.",
            "task": task_to_dict(task)
        }), 200

    except Exception as error:

        db.session.rollback()

        return jsonify({
            "message": "Could not complete task.",
            "error": str(error)
        }), 500


# ============================================================
# REGISTER ROUTES
# ============================================================

def register_volunteer_routes(app):

    app.register_blueprint(
        volunteer_bp
    )

    # Create VolunteerProfile table if it does not exist.
    with app.app_context():
        db.create_all()