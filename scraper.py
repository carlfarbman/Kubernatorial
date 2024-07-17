import requests
from bs4 import BeautifulSoup

# Send GET request to fetch page content
response = requests.get("https://kubernetes.io/docs/reference/glossary/?fundamental=true")

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all tags that may contain the required glossary terms under "fundamental"
    glossary_items = soup.select('li[data-show-count="0"]')

    # List of terms to include
    terms_to_include = [
        "Affinity", "Annotation", "API Group", "API server", "Applications", "cgroup (control group)",
        "Cluster", "Container", "Container Environment Variables", "Container Runtime",
        "Container runtime interface (CRI)", "Control Plane", "Controller", "CustomResourceDefinition",
        "DaemonSet", "Data Plane", "Deployment", "Device Plugin", "Disruption", "Docker",
        "Dockershim", "Ephemeral Container", "Event", "Extensions", "Feature gate", "Finalizer",
        "Garbage Collection", "Image", "Init Container", "Job", "kube-controller-manager",
        "kube-proxy", "Kubectl", "Kubelet", "Kubernetes API", "Label", "LimitRange", "Logging",
        "Manifest", "Master", "Minikube", "Mirror Pod", "Name", "Namespace", "Node", "Object",
        "Pod", "Pod Lifecycle", "Pod Security Policy", "QoS Class", "RBAC (Role-Based Access Control)",
        "Replica", "ReplicaSet", "Resource Quotas", "Selector", "Service", "ServiceAccount",
        "Shuffle-sharding", "Sidecar Container", "Spec", "StatefulSet", "Static Pod", "Taint",
        "Toleration", "UID", "Volume", "Workload"
    ]

    # Dictionary to hold only the fundamental vocab words
    glossary_terms = {}

    for item in glossary_items:
        # The term is contained in the 'b' tag within '.term-name'
        term = item.select_one('.term-name b').text

        # Check if the term is in the list of terms to include
        if term in terms_to_include:
            # The main definition comes after the term name, within 'span.preview-text'
            definition = item.select_one('span.preview-text').text.strip()

            # The supplemental definition, if it exists, is within the hidden next sibling div
            supplemental_div = item.select_one('div.hide')
            if supplemental_div:
                # Use `get_text()` to extract all text within supplemental_div, 
                # separating via `\n` and removing any excess whitespace
                supplemental_definition = supplemental_div.get_text(separator='\n', strip=True)
            else:
                supplemental_definition = ""

            # Store the definitions in the glossary dictionary using the term name as the key
            glossary_terms[term] = {
                'definition': definition,
                'supplemental_definition': supplemental_definition
            }

    # Display the content in the desired format
    for term, contents in glossary_terms.items():
        print("- - - - - - - - - - - - - - - - - ")
        print(f"Term: {term}")
        print(f"Definition: {contents['definition']}")
        supplemental = contents['supplemental_definition'].replace('\n', ' ')
        print(f"Supplemental definition: {supplemental}\n")
else:
    print(f"Failed to retrieve glossary. Status code: {response.status_code}")