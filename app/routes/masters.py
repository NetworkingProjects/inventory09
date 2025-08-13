from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from ..extensions import db, csrf
from ..models import (
    ROLE_SUPERADMIN, ROLE_ADMIN,
    Team, Manufacturer, VendorM, LocationM,
    Recipient, CategoryM, SubCategoryM
)
import json

masters_bp = Blueprint("masters", __name__, url_prefix="/masters")

def can_manage():
    return current_user.is_authenticated and current_user.role in (ROLE_SUPERADMIN, ROLE_ADMIN)

@masters_bp.route("/", methods=["GET"])
@login_required
def index():
    if not can_manage():
        flash("Admins only", "error")
        return redirect(url_for("assets.dashboard"))
    tab = request.args.get("tab", "team")
    teams = Team.query.order_by(Team.name.asc()).all()
    mans = Manufacturer.query.order_by(Manufacturer.name.asc()).all()
    vendors = VendorM.query.order_by(VendorM.name.asc()).all()
    locs = LocationM.query.order_by(LocationM.name.asc()).all()
    recips = Recipient.query.order_by(Recipient.name.asc()).all()
    cats = CategoryM.query.order_by(CategoryM.name.asc()).all()
    subcats = SubCategoryM.query.order_by(SubCategoryM.name.asc()).all()
    return render_template(
        "masters/index.html",
        tab=tab,
        teams=teams, mans=mans, vendors=vendors, locs=locs,
        recips=recips, cats=cats, subcats=subcats
    )

# ---------- helpers ----------
def _payload():
    """Accept JSON or form posts."""
    if request.is_json:
        data = request.get_json(silent=True) or {}
    elif request.form:
        data = request.form.to_dict()
    else:
        try:
            data = json.loads(request.data or b"") or {}
        except Exception:
            data = {}
    for k, v in list(data.items()):
        if isinstance(v, str):
            data[k] = v.strip()
    return data

def _created(payload): return jsonify(payload), 201
def _forbidden(): return jsonify({"error": "forbidden"}), 403
def _bad(msg="bad request"): return jsonify({"error": msg}), 400
def _exists(): return jsonify({"error": "exists"}), 409

def _model_for(kind):
    return {
        "team": Team,
        "manufacturer": Manufacturer,
        "vendor": VendorM,
        "location": LocationM,
        "recipient": Recipient,
        "category": CategoryM,
        "subcategory": SubCategoryM,
    }.get(kind)

# ---------- create ----------
@csrf.exempt
@masters_bp.post("/api/add/team")
@login_required
def api_add_team():
    if not can_manage(): return _forbidden()
    name = _payload().get("name") or ""
    if not name: return _bad("name required")
    if Team.query.filter_by(name=name).first(): return _exists()
    obj = Team(name=name)
    db.session.add(obj); db.session.commit()
    return _created({"id": obj.id, "name": obj.name})

@csrf.exempt
@masters_bp.post("/api/add/manufacturer")
@login_required
def api_add_manufacturer():
    if not can_manage(): return _forbidden()
    name = _payload().get("name") or ""
    if not name: return _bad("name required")
    if Manufacturer.query.filter_by(name=name).first(): return _exists()
    obj = Manufacturer(name=name)
    db.session.add(obj); db.session.commit()
    return _created({"id": obj.id, "name": obj.name})

@csrf.exempt
@masters_bp.post("/api/add/vendor")
@login_required
def api_add_vendor():
    if not can_manage(): return _forbidden()
    name = _payload().get("name") or ""
    if not name: return _bad("name required")
    if VendorM.query.filter_by(name=name).first(): return _exists()
    obj = VendorM(name=name)
    db.session.add(obj); db.session.commit()
    return _created({"id": obj.id, "name": obj.name})

@csrf.exempt
@masters_bp.post("/api/add/location")
@login_required
def api_add_location():
    if not can_manage(): return _forbidden()
    name = _payload().get("name") or ""
    if not name: return _bad("name required")
    if LocationM.query.filter_by(name=name).first(): return _exists()
    obj = LocationM(name=name)
    db.session.add(obj); db.session.commit()
    return _created({"id": obj.id, "name": obj.name})

@csrf.exempt
@masters_bp.post("/api/add/recipient")
@login_required
def api_add_recipient():
    if not can_manage(): return _forbidden()
    data = _payload()
    name = data.get("name") or ""
    email = data.get("email") or ""
    if not name or not email: return _bad("name and email required")
    if Recipient.query.filter_by(name=name, email=email).first(): return _exists()
    obj = Recipient(name=name, email=email)
    db.session.add(obj); db.session.commit()
    return _created({"id": obj.id, "name": obj.name, "email": obj.email})

@csrf.exempt
@masters_bp.post("/api/add/category")
@login_required
def api_add_category():
    if not can_manage(): return _forbidden()
    name = _payload().get("name") or ""
    if not name: return _bad("name required")
    if CategoryM.query.filter_by(name=name).first(): return _exists()
    obj = CategoryM(name=name)
    db.session.add(obj); db.session.commit()
    return _created({"id": obj.id, "name": obj.name})

@csrf.exempt
@masters_bp.post("/api/add/subcategory")
@login_required
def api_add_subcategory():
    if not can_manage(): return _forbidden()
    data = _payload()
    name = data.get("name") or ""
    category_id = data.get("category_id")
    if not name or not category_id: return _bad("name and category_id required")
    obj = SubCategoryM(name=name, category_id=int(category_id))
    db.session.add(obj); db.session.commit()
    return _created({"id": obj.id, "name": obj.name, "category_id": obj.category_id})

# ---------- read ----------
@masters_bp.get("/api/subcategories")
@login_required
def api_get_subcategories():
    category_id = request.args.get("category_id", type=int)
    if not category_id: return jsonify([])
    subs = SubCategoryM.query.filter_by(category_id=category_id).order_by(SubCategoryM.name.asc()).all()
    return jsonify([{"id": s.id, "name": s.name} for s in subs])

# ---------- update / delete ----------
@csrf.exempt
@masters_bp.post("/api/update/<kind>/<int:item_id>")
@login_required
def api_update(kind, item_id):
    if not can_manage(): return _forbidden()
    model = _model_for(kind)
    if not model: return _bad("invalid kind")
    obj = model.query.get_or_404(item_id)
    data = _payload()
    if kind == "recipient":
        name = data.get("name") or ""
        email = data.get("email") or ""
        if not name or not email: return _bad("name and email required")
        obj.name, obj.email = name, email
    else:
        name = data.get("name") or ""
        if not name: return _bad("name required")
        obj.name = name
    db.session.commit()
    return jsonify({"ok": True})

@csrf.exempt
@masters_bp.delete("/api/delete/<kind>/<int:item_id>")
@login_required
def api_delete(kind, item_id):
    if not can_manage(): return _forbidden()
    model = _model_for(kind)
    if not model: return _bad("invalid kind")
    obj = model.query.get_or_404(item_id)
    db.session.delete(obj); db.session.commit()
    return jsonify({"ok": True})
