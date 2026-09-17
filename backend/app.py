# pyrefly: ignore [missing-import]
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
# pyrefly: ignore [missing-import]
from flask_sqlalchemy import SQLAlchemy
# pyrefly: ignore [missing-import]
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    jwt_required,
    get_jwt_identity,
)
# pyrefly: ignore [missing-import]
from werkzeug.security import generate_password_hash, check_password_hash
# pyrefly: ignore [missing-import]
from werkzeug.utils import secure_filename

from datetime import datetime, timedelta
import os
import uuid


# ============================================================
# APP CONFIGURATION
# ============================================================

app = Flask(__name__)

CORS(
    app,
    resources={r"/api/*": {"origins": "*"}},
    supports_credentials=True,
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATABASE_PATH = os.path.join(BASE_DIR, "database.db")

UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"sqlite:///{DATABASE_PATH}"
)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config["JWT_SECRET_KEY"] = "resqlink-development-secret-change-later"

app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=24)

app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024


db = SQLAlchemy(app)

jwt = JWTManager(app)


# ============================================================
# DATABASE MODELS
# ============================================================


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(120), nullable=False)

    email = db.Column(
        db.String(150),
        unique=True,
        nullable=False,
        index=True,
    )

    phone = db.Column(db.String(30), nullable=True)

    password_hash = db.Column(db.String(255), nullable=False)

    role = db.Column(
        db.String(30),
        nullable=False,
        default="user",
    )

    location = db.Column(db.String(255), nullable=True)

    is_verified = db.Column(
        db.Boolean,
        default=False,
        nullable=False,
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
    )

    organizations = db.relationship(
        "Organization",
        backref="user",
        lazy=True,
        cascade="all, delete-orphan",
    )


class Organization(db.Model):
    __tablename__ = "organizations"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
    )

    organization_name = db.Column(
        db.String(200),
        nullable=False,
    )

    organization_type = db.Column(
        db.String(50),
        nullable=False,
    )

    address = db.Column(
        db.String(300),
        nullable=True,
    )

    verification_status = db.Column(
        db.String(30),
        default="pending",
        nullable=False,
    )

    documents = db.Column(
        db.String(500),
        nullable=True,
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
    )


class Donation(db.Model):
    __tablename__ = "donations"

    id = db.Column(db.Integer, primary_key=True)

    donor_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
    )

    category = db.Column(
        db.String(100),
        nullable=False,
    )

    item_name = db.Column(
        db.String(200),
        nullable=False,
    )

    quantity = db.Column(
        db.Integer,
        nullable=False,
        default=1,
    )

    condition = db.Column(
        db.String(50),
        nullable=True,
    )

    description = db.Column(
        db.Text,
        nullable=True,
    )

    location = db.Column(
        db.String(255),
        nullable=True,
    )

    donation_type = db.Column(
        db.String(50),
        nullable=True,
    )

    target_type = db.Column(
        db.String(50),
        nullable=True,
    )

    status = db.Column(
        db.String(50),
        default="available",
        nullable=False,
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
    )


class DonationImage(db.Model):
    __tablename__ = "donation_images"

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    donation_id = db.Column(
        db.Integer,
        db.ForeignKey("donations.id"),
        nullable=False,
    )

    filename = db.Column(
        db.String(255),
        nullable=False,
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
    )


class Requirement(db.Model):
    __tablename__ = "requirements"

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    organization_id = db.Column(
        db.Integer,
        db.ForeignKey("organizations.id"),
        nullable=False,
    )

    category = db.Column(
        db.String(100),
        nullable=False,
    )

    item_name = db.Column(
        db.String(200),
        nullable=False,
    )

    quantity_required = db.Column(
        db.Integer,
        nullable=False,
        default=1,
    )

    priority = db.Column(
        db.String(30),
        default="normal",
    )

    description = db.Column(
        db.Text,
        nullable=True,
    )

    location = db.Column(
        db.String(255),
        nullable=True,
    )

    status = db.Column(
        db.String(30),
        default="open",
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
    )


class Request(db.Model):
    __tablename__ = "requests"

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    donation_id = db.Column(
        db.Integer,
        db.ForeignKey("donations.id"),
        nullable=True,
    )

    requester_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
    )

    organization_id = db.Column(
        db.Integer,
        db.ForeignKey("organizations.id"),
        nullable=True,
    )

    status = db.Column(
        db.String(50),
        default="requested",
        nullable=False,
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
    )


class VolunteerTask(db.Model):
    __tablename__ = "volunteer_tasks"

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    volunteer_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
    )

    request_id = db.Column(
        db.Integer,
        db.ForeignKey("requests.id"),
        nullable=False,
    )

    pickup_location = db.Column(
        db.String(255),
        nullable=True,
    )

    delivery_location = db.Column(
        db.String(255),
        nullable=True,
    )

    status = db.Column(
        db.String(50),
        default="assigned",
        nullable=False,
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
    )


class BloodInventory(db.Model):
    __tablename__ = "blood_inventory"

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    organization_id = db.Column(
        db.Integer,
        db.ForeignKey("organizations.id"),
        nullable=False,
    )

    blood_group = db.Column(
        db.String(10),
        nullable=False,
    )

    units_available = db.Column(
        db.Integer,
        default=0,
        nullable=False,
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )


class BloodRequest(db.Model):
    __tablename__ = "blood_requests"

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    organization_id = db.Column(
        db.Integer,
        db.ForeignKey("organizations.id"),
        nullable=False,
    )

    blood_group = db.Column(
        db.String(10),
        nullable=False,
    )

    units_required = db.Column(
        db.Integer,
        nullable=False,
    )

    urgency = db.Column(
        db.String(30),
        default="normal",
    )

    patient_reference = db.Column(
        db.String(150),
        nullable=True,
    )

    hospital_name = db.Column(
        db.String(200),
        nullable=True,
    )

    contact_phone = db.Column(
        db.String(30),
        nullable=True,
    )

    status = db.Column(
        db.String(30),
        default="open",
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
    )


# ============================================================
# LOGIN HISTORY
# ============================================================

class LoginHistory(db.Model):
    __tablename__ = "login_history"

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
    )

    login_time = db.Column(
        db.DateTime,
        default=datetime.utcnow,
    )

    login_status = db.Column(
        db.String(30),
        default="success",
    )


# ============================================================
# HELPER FUNCTIONS
# ============================================================


def get_current_user():
    try:
        user_id = int(get_jwt_identity())
    except (TypeError, ValueError):
        return None

    return db.session.get(User, user_id)


def organization_to_dict(org):
    if not org:
        return None

    return {
        "id": org.id,
        "user_id": org.user_id,
        "organization_name": org.organization_name,
        "organization_type": org.organization_type,
        "address": org.address,
        "verification_status": org.verification_status,
        "documents": org.documents,
        "created_at": (
            org.created_at.isoformat()
            if org.created_at
            else None
        ),
    }


def user_to_dict(user):
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "phone": user.phone,
        "role": user.role,
        "location": user.location,
        "is_verified": user.is_verified,
        "created_at": (
            user.created_at.isoformat()
            if user.created_at
            else None
        ),
    }


# ============================================================
# HEALTH / ROOT
# ============================================================


@app.route("/", methods=["GET"])
def home():
    return jsonify(
        {
            "message": "ResQLink Platform Backend is Running!",
            "status": "success",
        }
    )


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify(
        {
            "status": "success",
            "message": "Backend and database are running.",
        }
    )


# ============================================================
# AUTHENTICATION
# ============================================================


@app.route("/api/auth/signup", methods=["POST"])
def signup():

    data = request.get_json(silent=True) or {}

    name = str(data.get("name", "")).strip()
    email = str(data.get("email", "")).strip().lower()
    phone = str(data.get("phone", "")).strip()
    password = data.get("password", "")
    role = str(data.get("role", "user")).strip().lower()

    location = str(
        data.get("location", "")
    ).strip()

    organization_name = str(
        data.get("organization_name", "")
    ).strip()

    organization_type = str(
        data.get("organization_type", "")
    ).strip()

    organization_address = str(
        data.get("organization_address", "")
    ).strip()

    # --------------------------------------------------------
    # VALIDATION
    # --------------------------------------------------------

    if not name:
        return jsonify(
            {"message": "Name is required."}
        ), 400

    if not email:
        return jsonify(
            {"message": "Email is required."}
        ), 400

    if not password:
        return jsonify(
            {"message": "Password is required."}
        ), 400

    if len(password) < 6:
        return jsonify(
            {
                "message": "Password must contain at least 6 characters."
            }
        ), 400

    allowed_roles = [
        "user",
        "volunteer",
        "ngo",
        "blood_bank",
    ]

    if role not in allowed_roles:
        return jsonify(
            {"message": "Invalid role."}
        ), 400

    existing_user = User.query.filter_by(
        email=email
    ).first()

    if existing_user:
        return jsonify(
            {
                "message": "An account with this email already exists."
            }
        ), 409

    # --------------------------------------------------------
    # ORGANIZATION VALIDATION
    # --------------------------------------------------------

    if role in ["ngo", "blood_bank"]:

        if not organization_name:
            return jsonify(
                {
                    "message": "Organization name is required."
                }
            ), 400

        if not organization_address:
            return jsonify(
                {
                    "message": "Organization address is required."
                }
            ), 400

        if role == "ngo":
            organization_type = "NGO"

        if role == "blood_bank":
            organization_type = "Blood Bank"

    # --------------------------------------------------------
    # USER CREATION
    # --------------------------------------------------------

    user = User(
        name=name,
        email=email,
        phone=phone or None,
        password_hash=generate_password_hash(password),
        role=role,
        location=location or None,
        is_verified=role in ["user", "volunteer"],
    )

    db.session.add(user)
    db.session.flush()

    # --------------------------------------------------------
    # ORGANIZATION CREATION
    # --------------------------------------------------------

    if role in ["ngo", "blood_bank"]:

        organization = Organization(
            user_id=user.id,
            organization_name=organization_name,
            organization_type=organization_type,
            address=organization_address,
            verification_status="pending",
            documents=None,
        )

        db.session.add(organization)

    db.session.commit()

    return jsonify(
        {
            "message": (
                "Registration successful. "
                "Organization accounts require admin verification."
                if role in ["ngo", "blood_bank"]
                else "Registration successful."
            ),
            "user": user_to_dict(user),
        }
    ), 201


@app.route("/api/auth/login", methods=["POST"])
def login():

    data = request.get_json(silent=True) or {}

    email = str(
        data.get("email", "")
    ).strip().lower()

    password = data.get("password", "")

    if not email or not password:
        return jsonify(
            {
                "message": "Email and password are required."
            }
        ), 400

    user = User.query.filter_by(
        email=email
    ).first()

    print(f"DEBUG LOGIN - Email: '{email}', Found user: {user.email if user else None}", flush=True)
    if user:
        pwd_ok = check_password_hash(user.password_hash, password)
        print(f"DEBUG LOGIN - Password match: {pwd_ok}", flush=True)

    if not user:
        return jsonify(
            {
                "message": "Invalid email or password."
            }
        ), 401

    if not check_password_hash(
        user.password_hash,
        password,
    ):
        return jsonify(
            {
                "message": "Invalid email or password."
            }
        ), 401

    # --------------------------------------------------------
    # ORGANIZATION VERIFICATION CHECK
    # --------------------------------------------------------

    organization = Organization.query.filter_by(
        user_id=user.id
    ).first()

    if user.role in ["ngo", "blood_bank"]:

        if not organization:
            return jsonify(
                {
                    "message": "Organization profile not found."
                }
            ), 403

        if organization.verification_status != "verified":

            return jsonify(
                {
                    "message": (
                        "Your organization is waiting for "
                        "admin verification."
                    ),
                    "verification_status": (
                        organization.verification_status
                    ),
                }
            ), 403

    # --------------------------------------------------------
    # CREATE LOGIN HISTORY
    # --------------------------------------------------------

    history = LoginHistory(
        user_id=user.id,
        login_status="success",
    )

    db.session.add(history)

    db.session.commit()

    # --------------------------------------------------------
    # JWT
    # --------------------------------------------------------

    access_token = create_access_token(
        identity=str(user.id)
    )

    return jsonify(
        {
            "message": "Login successful.",
            "access_token": access_token,
            "token": access_token,
            "user": user_to_dict(user),
            "organization": organization_to_dict(
                organization
            ),
        }
    ), 200


@app.route("/api/auth/me", methods=["GET"])
@jwt_required()
def current_user():

    user = get_current_user()

    if not user:
        return jsonify(
            {"message": "User not found."}
        ), 404

    organization = Organization.query.filter_by(
        user_id=user.id
    ).first()

    return jsonify(
        {
            "user": user_to_dict(user),
            "organization": organization_to_dict(
                organization
            ),
        }
    )


# ============================================================
# PUBLIC ORGANIZATIONS
# ============================================================


@app.route("/api/organizations", methods=["GET"])
def get_organizations():

    organizations = Organization.query.filter_by(
        verification_status="verified"
    ).order_by(
        Organization.created_at.desc()
    ).all()

    result = []

    for org in organizations:

        result.append(
            organization_to_dict(org)
        )

    return jsonify(
        {
            "organizations": result,
            "count": len(result),
        }
    )


# ============================================================
# ORGANIZATION REQUIREMENTS
# ============================================================


@app.route("/api/requirements", methods=["GET"])
def get_requirements():

    requirements = Requirement.query.filter_by(
        status="open"
    ).order_by(
        Requirement.created_at.desc()
    ).all()

    result = []

    for requirement in requirements:

        organization = db.session.get(
            Organization,
            requirement.organization_id,
        )

        result.append(
            {
                "id": requirement.id,
                "organization_id": requirement.organization_id,
                "organization_name": (
                    organization.organization_name
                    if organization
                    else "Organization"
                ),
                "category": requirement.category,
                "item_name": requirement.item_name,
                "quantity_required": (
                    requirement.quantity_required
                ),
                "priority": requirement.priority,
                "description": requirement.description,
                "location": requirement.location,
                "status": requirement.status,
                "created_at": (
                    requirement.created_at.isoformat()
                    if requirement.created_at
                    else None
                ),
            }
        )

    return jsonify(
        {
            "requirements": result,
            "count": len(result),
        }
    )


# ============================================================
# DONATIONS
# ============================================================


@app.route("/api/donations", methods=["POST"])
@jwt_required()
def create_donation():

    user = get_current_user()

    if not user:
        return jsonify(
            {"message": "User not found."}
        ), 404

    category = str(
        request.form.get("category", "")
    ).strip()

    item_name = str(
        request.form.get("item_name", "")
    ).strip()

    condition = str(
        request.form.get("condition", "")
    ).strip()

    description = str(
        request.form.get("description", "")
    ).strip()

    location = str(
        request.form.get("location", "")
    ).strip()

    donation_type = str(
        request.form.get("donation_type", "")
    ).strip()

    target_type = str(
        request.form.get("target_type", "")
    ).strip()

    try:
        quantity = int(
            request.form.get("quantity", 1)
        )
    except ValueError:
        quantity = 1

    if not category:
        return jsonify(
            {"message": "Category is required."}
        ), 400

    if not item_name:
        return jsonify(
            {"message": "Item name is required."}
        ), 400

    if quantity < 1:
        return jsonify(
            {"message": "Quantity must be at least 1."}
        ), 400

    donation = Donation(
        donor_id=user.id,
        category=category,
        item_name=item_name,
        quantity=quantity,
        condition=condition,
        description=description,
        location=location,
        donation_type=donation_type,
        target_type=target_type,
        status="available",
    )

    db.session.add(donation)
    db.session.flush()

    # --------------------------------------------------------
    # IMAGE UPLOAD
    # --------------------------------------------------------

    uploaded_files = request.files.getlist(
        "images"
    )

    uploaded_files = uploaded_files[:5]

    for file in uploaded_files:

        if not file or not file.filename:
            continue

        original_name = secure_filename(
            file.filename
        )

        extension = ""

        if "." in original_name:
            extension = "." + original_name.rsplit(
                ".",
                1,
            )[1].lower()

        filename = (
            f"{uuid.uuid4().hex}"
            f"{extension}"
        )

        file.save(
            os.path.join(
                UPLOAD_FOLDER,
                filename,
            )
        )

        image = DonationImage(
            donation_id=donation.id,
            filename=filename,
        )

        db.session.add(image)

    db.session.commit()

    return jsonify(
        {
            "message": "Donation created successfully.",
            "donation": {
                "id": donation.id,
                "category": donation.category,
                "item_name": donation.item_name,
                "quantity": donation.quantity,
                "condition": donation.condition,
                "description": donation.description,
                "location": donation.location,
                "donation_type": donation.donation_type,
                "target_type": donation.target_type,
                "status": donation.status,
            },
        }
    ), 201


@app.route("/api/donations", methods=["GET"])
def get_donations():

    donations = Donation.query.order_by(
        Donation.created_at.desc()
    ).all()

    result = []

    for donation in donations:

        images = DonationImage.query.filter_by(
            donation_id=donation.id
        ).all()

        result.append(
            {
                "id": donation.id,
                "donor_id": donation.donor_id,
                "category": donation.category,
                "item_name": donation.item_name,
                "quantity": donation.quantity,
                "condition": donation.condition,
                "description": donation.description,
                "location": donation.location,
                "donation_type": donation.donation_type,
                "target_type": donation.target_type,
                "status": donation.status,
                "created_at": (
                    donation.created_at.isoformat()
                    if donation.created_at
                    else None
                ),
                "images": [
                    {
                        "id": image.id,
                        "filename": image.filename,
                        "url": (
                            f"/uploads/{image.filename}"
                        ),
                    }
                    for image in images
                ],
            }
        )

    return jsonify(
        {
            "donations": result,
            "count": len(result),
        }
    )


@app.route("/api/donations/my", methods=["GET"])
@jwt_required()
def get_my_donations():

    user = get_current_user()

    if not user:
        return jsonify(
            {"message": "User not found."}
        ), 404

    donations = Donation.query.filter_by(
        donor_id=user.id
    ).order_by(
        Donation.created_at.desc()
    ).all()

    result = []

    for donation in donations:

        result.append(
            {
                "id": donation.id,
                "category": donation.category,
                "item_name": donation.item_name,
                "quantity": donation.quantity,
                "condition": donation.condition,
                "description": donation.description,
                "location": donation.location,
                "donation_type": donation.donation_type,
                "target_type": donation.target_type,
                "status": donation.status,
                "created_at": (
                    donation.created_at.isoformat()
                    if donation.created_at
                    else None
                ),
            }
        )

    return jsonify(
        {
            "donations": result,
            "count": len(result),
        }
    )


# ============================================================
# DONATION REQUEST
# ============================================================


@app.route("/api/donations/<int:donation_id>/request", methods=["POST"])
@jwt_required()
def request_donation(donation_id):

    user = get_current_user()

    if not user:
        return jsonify(
            {"message": "User not found."}
        ), 404

    donation = db.session.get(
        Donation,
        donation_id,
    )

    if not donation:
        return jsonify(
            {"message": "Donation not found."}
        ), 404

    if donation.status != "available":
        return jsonify(
            {
                "message": "This donation is no longer available."
            }
        ), 400

    if donation.donor_id == user.id:
        return jsonify(
            {
                "message": "You cannot request your own donation."
            }
        ), 400

    new_request = Request(
        donation_id=donation.id,
        requester_id=user.id,
        status="requested",
    )

    db.session.add(new_request)

    donation.status = "requested"

    db.session.commit()

    return jsonify(
        {
            "message": "Donation requested successfully.",
            "request_id": new_request.id,
        }
    ), 201


# ============================================================
# UPLOADS
# ============================================================


@app.route("/uploads/<path:filename>", methods=["GET"])
def uploaded_file(filename):

    return send_from_directory(
        UPLOAD_FOLDER,
        filename,
    )


# ============================================================
# ADMIN
# ============================================================


@app.route("/api/admin/users", methods=["GET"])
@jwt_required()
def admin_users():

    user = get_current_user()

    if not user:
        return jsonify(
            {"message": "User not found."}
        ), 404

    if user.role != "admin":
        return jsonify(
            {"message": "Admin access required."}
        ), 403

    users = User.query.order_by(
        User.created_at.desc()
    ).all()

    return jsonify(
        {
            "users": [
                user_to_dict(account)
                for account in users
            ],
            "count": len(users),
        }
    )


@app.route("/api/admin/login-history", methods=["GET"])
@jwt_required()
def admin_login_history():

    user = get_current_user()

    if not user:
        return jsonify(
            {"message": "User not found."}
        ), 404

    if user.role != "admin":
        return jsonify(
            {"message": "Admin access required."}
        ), 403

    history = LoginHistory.query.order_by(
        LoginHistory.login_time.desc()
    ).limit(100).all()

    result = []

    for record in history:

        account = db.session.get(
            User,
            record.user_id,
        )

        result.append(
            {
                "id": record.id,
                "user_id": record.user_id,
                "user_name": (
                    account.name
                    if account
                    else "Unknown"
                ),
                "user_email": (
                    account.email
                    if account
                    else "Unknown"
                ),
                "login_time": (
                    record.login_time.isoformat()
                    if record.login_time
                    else None
                ),
                "login_status": record.login_status,
            }
        )

    return jsonify(
        {
            "history": result,
            "count": len(result),
        }
    )


# ============================================================
# ORGANIZATION APPROVAL
# ============================================================


@app.route(
    "/api/accounts/pending-verifications",
    methods=["GET"],
)
@jwt_required()
def pending_verifications():

    user = get_current_user()

    if not user or user.role != "admin":
        return jsonify(
            {"message": "Admin access required."}
        ), 403

    organizations = Organization.query.filter_by(
        verification_status="pending"
    ).order_by(
        Organization.created_at.asc()
    ).all()

    result = []

    for organization in organizations:

        account = db.session.get(
            User,
            organization.user_id,
        )

        data = organization_to_dict(
            organization
        )

        data["name"] = (
            account.name
            if account
            else None
        )

        data["email"] = (
            account.email
            if account
            else None
        )

        data["phone"] = (
            account.phone
            if account
            else None
        )

        data["role"] = (
            account.role
            if account
            else None
        )

        result.append(data)

    return jsonify(
        {
            "organizations": result,
            "count": len(result),
        }
    )


@app.route(
    "/api/accounts/pending-verifications/<int:organization_id>/approve/",
    methods=["POST"],
)
@jwt_required()
def approve_organization(organization_id):

    user = get_current_user()

    if not user or user.role != "admin":
        return jsonify(
            {"message": "Admin access required."}
        ), 403

    organization = db.session.get(
        Organization,
        organization_id,
    )

    if not organization:
        return jsonify(
            {"message": "Organization not found."}
        ), 404

    organization.verification_status = "verified"

    account = db.session.get(
        User,
        organization.user_id,
    )

    if account:
        account.is_verified = True

    db.session.commit()

    return jsonify(
        {
            "message": "Organization approved successfully.",
            "organization": organization_to_dict(
                organization
            ),
        }
    )


@app.route(
    "/api/accounts/pending-verifications/<int:organization_id>/reject/",
    methods=["POST"],
)
@jwt_required()
def reject_organization(organization_id):

    user = get_current_user()

    if not user or user.role != "admin":
        return jsonify(
            {"message": "Admin access required."}
        ), 403

    organization = db.session.get(
        Organization,
        organization_id,
    )

    if not organization:
        return jsonify(
            {"message": "Organization not found."}
        ), 404

    organization.verification_status = "rejected"

    account = db.session.get(
        User,
        organization.user_id,
    )

    if account:
        account.is_verified = False

    db.session.commit()

    return jsonify(
        {
            "message": "Organization rejected.",
            "organization": organization_to_dict(
                organization
            ),
        }
    )


# ============================================================
# REGISTER OPTIONAL ROLE ROUTES
# ============================================================

try:
    from volunteer_routes import register_volunteer_routes

    register_volunteer_routes(app)

except Exception as error:

    print(
        "VOLUNTEER ROUTES ERROR:",
        error,
    )


try:
    from ngo_routes import register_ngo_routes

    register_ngo_routes(app)

except Exception as error:

    print(
        "NGO ROUTES ERROR:",
        error,
    )


try:
    from blood_routes import register_blood_routes

    register_blood_routes(app)

except Exception as error:

    print(
        "BLOOD ROUTES ERROR:",
        error,
    )


# ============================================================
# DATABASE INITIALIZATION
# ============================================================


with app.app_context():

    db.create_all()


# ============================================================
# START SERVER
# ============================================================


if __name__ == "__main__":

    print()
    print("=" * 60)
    print("        ResQLink Platform Backend")
    print("=" * 60)
    print(f"Database : {DATABASE_PATH}")
    print(f"Uploads  : {UPLOAD_FOLDER}")
    print("Server   : http://127.0.0.1:5000")
    print("=" * 60)
    print()

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True,
        use_reloader=False,
    )