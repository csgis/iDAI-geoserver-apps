import json
from collections import OrderedDict
import logging
logger = logging.getLogger("geonode")
import urllib.request
import json

def count_bones(instance):
    amount_of_bones = len(getattr(instance, "inventory", 0))
    return amount_of_bones

def get_bone_names(instance):

    inventory = getattr(instance, "inventory", {})
    if type(inventory) == str:
        inventory = json.loads(inventory)

    bone_names = ', '.join(x for x, y in inventory.items())
    return bone_names

def get_svgids(instance):
    inventory = getattr(instance, "inventory", {})
    bone_relations = getattr(instance, "bone_relations", {})
    amount_urlencode = {}

    if isinstance(bone_relations, str):
        bone_relations = json.loads(bone_relations)

    amount = {
        ">75%": [], # above or below 75 but without bone change
        "<75%": [], # above or below 75 but without bone change
        "affected": [], # above or below 75 but with bone change
        "unknown": []
    }

    bone_relations_key = bone_relations.keys()

    for item in inventory:
        amount_name = inventory[item]['amount'].lower()
        item_id = str(inventory[item]['id'])
        is_affected = False

        # check if bone has unknown or absent bones if no it is affected
        if item_id in bone_relations_key:
            changes = bone_relations[item_id]['_changes']
            for change in changes:
                # Check if there are other words besides the specified keywords
                if any(keyword.lower() not in ['absent', 'unknown', 'not applied'] for keyword in change['bone_change']):
                    # If other words are found, set is_affected to True and exit the loop
                    is_affected = True
                    break

        # Catch affected changes for above or below 75%
        if amount_name == '>75%' or amount_name == '<75%':
            amount_name = 'affected' if is_affected else amount_name

        # combine absent, unknown and not applied
        if amount_name in ['absent', 'unknown', 'not applied']:
            amount_name = 'unknown'

        svg_ids = inventory[item]['svgid'] \
            .replace('bone', '') \
            .split(',')

        for id in svg_ids:
            if id not in amount[amount_name]:
                amount[amount_name].append(id)

        amount_json = json.dumps(amount)
        amount_urlencode = urllib.parse.quote(amount_json)
    return amount_urlencode


def replace_all(text, dic):
    for i, j in dic.items():
        text = text.replace(i, j)
    return text


def format_bone_relations(instance):
    inventory = getattr(instance, "inventory", {})
    bone_relations = getattr(instance, "bone_relations", {})

    html_output = '<div class="bone-relations">'
    
    for key, item in inventory.items():
        label = item["label"]
        if label in ("Deciduous teeth", "Permanent teeth"):
            # Safely try to get the bone_change object by item["id"]
            bone_change = bone_relations.get(str(item["id"]))
            if bone_change:
                try:
                    # Extract the first digits from the bone_change label safely
                    digits_label = bone_change.get("label", "")
                    digits = digits_label.split(" ")[0] if digits_label else "Unknown ID"
                    item_name = f'{digits} ({label})'
                except Exception as e:
                    # In case of an error, fallback to using "Unknown ID"
                    print(f"Error extracting digits from bone_change label: {e}")
                    item_name = f'Unknown ID ({label})'
            else:
                # Fallback to item["id"] if bone_change is not found
                item_name = f'{item["id"]} ({label})'
        else:
            item_name = f'{label} ({item["section"].replace("_", " ")})'

        amount = item.get("amount", "Unknown amount")
        
        # Start item container with item name
        html_output += f'<div class="bone-item"><span class="item-name">{item_name}:</span>'
        
        # Create a list for amount
        html_output += '<ul class="item-details">'
        # Add amount as a list item
        html_output += f'<li>Amount: {amount}</li>'
        
        # Process changes if available
        if key in bone_relations:
            changes = bone_relations[key].get("_changes", "")
            if changes:
                for change in changes:
                    technic = change.get('technic', 'Unknown')
                    # Add technic as a list item with a sublist for bone changes
                    html_output += f'<li>Technique: {technic}<ul class="bone-changes">'
                    
                    bone_changes = change['bone_change']
                    if bone_changes == ['Not applied']:  # Check if bone_changes only contains 'Not applied'
                        # Directly add 'Not applied' without 'Bone change' prefix
                        html_output += f'<li>Not applied</li></ul></li>'
                    else:
                        bone_changes_text = ', '.join(bone_changes).rstrip(', ')
                        # Add each bone change within the technic's sublist
                        html_output += f'<li>Bone change: {bone_changes_text}</li></ul></li>'
        
        # Close list and item container
        html_output += '</ul></div>'
    
    # Close main container
    html_output += '</div>'
    
    return html_output


def get_technics(instance):
    bone_relations = getattr(instance, "bone_relations", {})
    technic = []
    for key in bone_relations.keys():
        changes_key = bone_relations[key].get("_changes")
        if (changes_key is not None):
          for change_item in changes_key:
              item = change_item.get("technic", None)
              if item is not None:
              	technic.append(item)

    technic = set(technic)
    technic = ', '.join(technic)
    return technic
