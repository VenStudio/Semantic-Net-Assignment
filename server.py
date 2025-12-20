from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from semantic_net import SemanticNet
import json
import base64
import os

VERSION = "0.2"
app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)

net = SemanticNet()
PRESETS_DIR = "./presets"

# load json file
def load_json(filepath):
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
    
        global net
        net = SemanticNet()
    
        # Load Nodes (with colors/metadata)
        net_data = data.get("graph", {})

        for n in data["nodes"]:
            net.add_node(n)

        for n in net_data.get("nodes", []):
            net.add_node(
                n.get("id"),
                color=n.get("color", "#808080"))

        # Load Edges
        for e in net_data.get("edges", []):
            net.add_relation(
                e.get("source"),
                e.get("relation"),
                e.get("target"),
                type=e.get("type", "manual"),
                inferred=e.get("dashes", False)
                )
        
        return True

    except Exception as e:
        print(f"Error loading file: {e}")
        return False

@app.route("/")
def index():
    return render_template("index.html")

# Project Management (Presets)
@app.route("/get_presets")
def get_presets():
    files = []
    for f in os.listdir(PRESETS_DIR):
        if not f.endswith(".json"):
            continue
        
        try:
            with open(os.path.join(PRESETS_DIR, f), "r") as file:
                data = json.load(file)
        
            meta = data.get("meta", {})
            files.append({
                "filename": f,
                "name": meta.get("name", "Untitled"),
                "has_preview": meta.get("thumbnail") is not None
            })
        except:
            continue

    return jsonify(files)

@app.route("/export_json", methods=["POST"])
def export_json():
    data = request.json

    # Extract pieces from the frontend request
    name = data.get("name", "Untitled")
    thumbnail_b64 = data.get("img_data", "") # The Base64 string from canvas
    palette = data.get("palette", [])        # Frontend must send the current palette colors
    nodes = data.get("nodes", [])            # Frontend sends current node state
    edges = data.get("edges", [])            # Frontend sends current edge state

    # Construct the exact JSON structure you defined
    export_data = {
        "meta": {
            "name": name,
            "version": VERSION,
            "thumbnail": thumbnail_b64  # Baked directly into the JSON
        },
        "settings": {
            "palette": palette
        },
        "graph": {
            "nodes": nodes,
            "edges": edges
        }
    }

    # Save JSON
    file_path = os.path.join(PRESETS_DIR, f"{name}.json")
    with open(file_path, "w") as f:
        json.dump(export_data, f, indent=2)
    
    return jsonify({"success": True})

@app.route("/import_json", methods=["POST"])
def import_json():
    filename = request.json.get("filename")
    path = os.path.join(PRESETS_DIR, filename)
    if load_json(path):
        return jsonify({"success": True})
    return jsonify({"error": f"{filename} not found"}), 404

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

# Initialize with default
load_json(os.path.join(PRESETS_DIR, "default.json"))

if __name__ == "__main__":
    app.run()

