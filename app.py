from flask import Flask, jsonify, request, render_template, send_from_directory
from semantic_net import SemanticNet
from project_manager import ProjectManager

VERSION = "0.2"
app = Flask(__name__, template_folder="templates", static_folder="static", static_url_path="/static")

PROJECTS_DIR = "./projects"
pm = ProjectManager(PROJECTS_DIR)
net = SemanticNet()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_version")
def get_version():
    return VERSION

# Serve projects (images and json)
@app.route('/projects/<path:filename>')
def serve_projects(filename):
    return send_from_directory(PROJECTS_DIR, filename)

# Project Management (Presets)
@app.route("/get_projects")
def get_projects():
    return jsonify(pm.get_projects())

@app.route("/load", methods=["POST"])
def load_project():
    filename = request.json.get("filename")
    global net
    loaded_net = pm.load_project(filename)
    
    if loaded_net:
        net = loaded_net
        return jsonify({"success": True})
    else:
        return jsonify({"success": False, "error": "Failed to load project"}), 400

@app.route("/save", methods=["POST"])
def save_project():
    data = request.json

    # Construct the exact JSON structure we want to save
    save_data = {
        "name": data.get("name", ""),
        "version": VERSION,
        "created_at": data.get("created_at", ""),
        "preview_b64": data.get("preview_b64", ""),
        "palette": data.get("palette", []),
        "nodes": data.get("nodes", []),
        "edges": data.get("edges", [])
    }

    pm.save_to_projects(save_data)
    
    return jsonify({"success": True})

@app.route("/export", methods=["POST"])
def export_project():
    data = request.json

    # Construct the exact JSON structure we want to save
    export_data = {
        "name": data.get("name", ""), # This field will be inherented by the actual filename when imported
        "version": VERSION,
        "preview_b64": data.get("preview_b64", ""),
        "palette": data.get("palette", []),
        "nodes": data.get("nodes", []),
        "edges": data.get("edges", [])
    }
    
    return jsonify({"success": True})

# Graph Operations
@app.route("/get_graph")
def get_graph():
    return jsonify(net.get_graph_data())

@app.route("/add_node", methods=["POST"])
def add_node():
    data = request.json
    net.add_node(data.get("name"), color=data.get("color"))
    return jsonify({"success": True})

@app.route("/add_relation", methods=["POST"])
def add_relation():
    data = request.json
    net.add_relation(data.get("source"), data.get("relation"), data.get("target"))
    
    inference_count = net.check_inference_potential()

    return jsonify({
        "success": True,
        "inference_count": inference_count
    })

@app.route("/remove_node", methods=["POST"])
def remove_node():
    data = request.json
    net.remove_node(data.get("name"))
    return jsonify({"success": True})

@app.route("/remove_relation", methods=["POST"])
def remove_relation():
    data = request.json
    net.remove_relation(data.get("source"), data.get("relation"), data.get("target"))
    return jsonify({"success": True})

@app.route("/inference", methods=["POST"])
def inference():
    new_edges, conflicts = net.run_inference()
    return jsonify({"new_edges": new_edges, "conflicts": conflicts})

@app.route("/check_inference")
def check_inference():
    count = net.check_inference_potential()
    return jsonify({"count": count})

if __name__ == "__main__":
    app.run(port=4300, debug=True)

