import google.generativeai as genai
from rdkit import Chem
from rdkit.Chem import Draw
from google_api_key import google_api_key
from io import BytesIO
from PIL import Image


def configure_genai(api_key):
    """Configure the Gemini AI API with the provided API key."""
    genai.configure(api_key=google_api_key)


def setup_model():
    """Set up the Gemini AI model with the specified configuration."""
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 0,
        "max_output_tokens": 100
    }
    return genai.GenerativeModel("gemini-1.5-flash", generation_config=generation_config)


def generate_smiles(compound_name, model):
    """Generate the SMILES notation for the given compound name using the Gemini model."""
    response = model.generate_content(
        # f"Give me the SMILES notation of compound only, don't mention anything else. If the input is a reaction, list the SMILES notations for the products. List each SMILES notation for the compound or reaction named '{compound_name}.")
        f"you are a chemical scientist.Extract and list ly the SMILES notations for all compounds involved in the given text or reaction name.don't mention anything else\
        If a reaction name  provided, perform the reaction and list the SMILES notations for both reactants and products. Do not include any ditional text or explanations. Provide each SMILES notation on a new line.\
        if compounds names are given then also include there products SMILES notation if feasable reaction between them is possible.generate SMILES notation suitable to parse by RDKit library only\
        Reaction or compound description: {compound_name}")
    print(response)
    response_text = response.text.strip()
    print(response_text.split())
    return response_text.split()


def generate_molecular_image(smiles_string):
    """Generate a molecular structure image from the given SMILES string."""
    mol = Chem.MolFromSmiles(smiles_string)
    if mol:
        img = Draw.MolToImage(mol)
        return img
    else:
        raise ValueError("Could not generate a chemical structure. Please check the SMILES notation.")


def get_compound_structure(api_key, compound_name):
    """Get the SMILES notation and molecular structure image for the given compound name."""
    configure_genai(api_key)
    model = setup_model()

    smiles_strings = generate_smiles(compound_name, model)
    images = []
    for smiles in smiles_strings:
        try:
            img_bytes = generate_molecular_image(smiles)
            images.append(img_bytes)
        except ValueError as e:
            print(e)

    return  images

# if __name__ == "__main__":
#     images = get_compound_structure(google_api_key, "water and aluminium")
#
#    # Display results
#     for img in images:
#         img.show()