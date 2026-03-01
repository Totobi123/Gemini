import os
import shutil
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, abort

app = Flask(__name__)

# Base directory for the file manager
BASE_DIR = os.path.abspath("/root")

RESTRICTED_PATHS = [
    "/root/gemini-bridge/venv",
    "/root/gemini-bridge/bridge.py",
    "/etc/systemd/system/gemini-bridge.service"
]

def is_restricted(path):
    abs_path = os.path.abspath(path)
    for restricted in RESTRICTED_PATHS:
        if abs_path == restricted or abs_path.startswith(restricted + os.sep):
            return True
    return False

def get_full_path(relative_path):
    # Ensure the path is within the base directory
    full_path = os.path.abspath(os.path.join(BASE_DIR, relative_path.lstrip("/")))
    if not full_path.startswith(BASE_DIR):
        abort(403)
    return full_path

@app.route("/")
def index():
    path = request.args.get("path", "").strip("/")
    full_path = get_full_path(path)
    
    if not os.path.exists(full_path):
        return "Path not found", 404
        
    # Breadcrumbs logic
    breadcrumbs = []
    parts = path.split("/") if path else []
    curr = ""
    for part in parts:
        curr = os.path.join(curr, part)
        breadcrumbs.append({"name": part, "path": curr})

    items = []
    # Add ".." if not at root
    if path:
        parent_path = os.path.dirname(path)
        items.append({"name": "..", "is_dir": True, "size": "-", "rel_path": parent_path, "restricted": False})
    else:
        parent_path = ""

    try:
        dir_contents = sorted(os.listdir(full_path))
    except PermissionError:
        return "Permission Denied", 403

    for name in dir_contents:
        item_full_path = os.path.join(full_path, name)
        is_dir = os.path.isdir(item_full_path)
        item_rel_path = os.path.join(path, name)
        restricted = is_restricted(item_full_path)
        size = "-"
        if not is_dir:
            try:
                size_bytes = os.path.getsize(item_full_path)
                for unit in ['B', 'KB', 'MB', 'GB']:
                    if size_bytes < 1024:
                        size = f"{size_bytes:.1f} {unit}"
                        break
                    size_bytes /= 1024
            except (PermissionError, FileNotFoundError):
                size = "N/A"
        
        items.append({
            "name": name,
            "is_dir": is_dir,
            "size": size,
            "rel_path": item_rel_path,
            "restricted": restricted
        })
        
    return render_template("index.html", items=items, current_path=path, breadcrumbs=breadcrumbs)

@app.route("/upload", methods=["POST"])
def upload():
    path = request.form.get("path", "")
    full_path = get_full_path(path)
    if is_restricted(full_path):
        abort(403)
    if "file" not in request.files:
        return "No file part", 400
    file = request.files["file"]
    if file.filename == "":
        return "No selected file", 400
    file.save(os.path.join(full_path, file.filename))
    return redirect(url_for("index", path=path))

@app.route("/create-folder", methods=["POST"])
def create_folder():
    path = request.form.get("path", "")
    name = request.form.get("name")
    full_path = get_full_path(path)
    target_path = os.path.join(full_path, name)
    if is_restricted(target_path):
        abort(403)
    os.makedirs(target_path, exist_ok=True)
    return redirect(url_for("index", path=path))

@app.route("/create-file", methods=["POST"])
def create_file():
    path = request.form.get("path", "")
    name = request.form.get("name")
    full_path = get_full_path(path)
    target_path = os.path.join(full_path, name)
    if is_restricted(target_path):
        abort(403)
    with open(target_path, "w") as f:
        pass
    return redirect(url_for("index", path=path))

@app.route("/rename", methods=["POST"])
def rename():
    path = request.form.get("path", "")
    old_name = request.form.get("old_name")
    new_name = request.form.get("new_name")
    full_path = get_full_path(path)
    old_path = os.path.join(full_path, old_name)
    new_path = os.path.join(full_path, new_name)
    if is_restricted(old_path) or is_restricted(new_path):
        abort(403)
    os.rename(old_path, new_path)
    return redirect(url_for("index", path=path))

@app.route("/move", methods=["POST"])
def move():
    path = request.form.get("path", "")
    name = request.form.get("name")
    dest_rel_path = request.form.get("dest_path")
    full_path = get_full_path(path)
    src_path = os.path.join(full_path, name)
    dest_path = get_full_path(dest_rel_path)
    
    if is_restricted(src_path) or is_restricted(dest_path):
        abort(403)
        
    shutil.move(src_path, os.path.join(dest_path, name))
    return redirect(url_for("index", path=path))

@app.route("/delete", methods=["POST"])
def delete():
    path = request.form.get("path", "")
    name = request.form.get("name")
    full_path = get_full_path(path)
    item_path = os.path.join(full_path, name)
    if is_restricted(item_path):
        abort(403)
    if os.path.isdir(item_path):
        shutil.rmtree(item_path)
    else:
        os.remove(item_path)
    return redirect(url_for("index", path=path))


@app.route("/download/<path:filename>")
def download(filename):
    full_path = get_full_path(os.path.dirname(filename))
    name = os.path.basename(filename)
    return send_from_directory(full_path, name, as_attachment=True)

@app.route("/view/<path:filename>")
def view(filename):
    full_path = get_full_path(os.path.dirname(filename))
    name = os.path.basename(filename)
    return send_from_directory(full_path, name, as_attachment=False)

if __name__ == "__main__":
    if not os.path.exists(BASE_DIR):
        os.makedirs(BASE_DIR)
    app.run(host="0.0.0.0", port=9000)
