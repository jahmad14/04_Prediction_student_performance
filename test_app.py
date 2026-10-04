import os
import sys
from streamlit.testing.v1 import AppTest

def test_regression_doc1_app():
    dep_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(dep_dir)
    
    print(f"Testing app.py in: {dep_dir}")
    
    # 1. Premier test : profil moyen
    at1 = AppTest.from_file("app.py", default_timeout=30)
    at1.run()
    assert len(at1.exception) == 0, f"Exception initialisation 1 : {at1.exception}"
    
    # Renseigner le formulaire 1
    at1.number_input[0].set_value(5.0)
    at1.number_input[1].set_value(70.0)
    at1.selectbox[0].select("No")
    at1.number_input[2].set_value(7.0)
    at1.number_input[3].set_value(3.0)
    at1.button[0].click().run()
    
    assert len(at1.exception) == 0, f"Exception prédiction 1 : {at1.exception}"
    assert len(at1.success) > 0, "Aucun message de succès trouvé après prédiction 1"
    pred1_text = at1.success[0].value
    print(f"Résultat Test 1 : {pred1_text}")
    
    # 2. Deuxième test : profil élevé
    at2 = AppTest.from_file("app.py", default_timeout=30)
    at2.run()
    assert len(at2.exception) == 0, f"Exception initialisation 2 : {at2.exception}"
    
    at2.number_input[0].set_value(9.0)
    at2.number_input[1].set_value(95.0)
    at2.selectbox[0].select("Yes")
    at2.number_input[2].set_value(8.0)
    at2.number_input[3].set_value(8.0)
    at2.button[0].click().run()
    
    assert len(at2.exception) == 0, f"Exception prédiction 2 : {at2.exception}"
    assert len(at2.success) > 0, "Aucun message de succès trouvé après prédiction 2"
    pred2_text = at2.success[0].value
    print(f"Résultat Test 2 : {pred2_text}")
    
    assert pred1_text != pred2_text, f"Les deux prédictions sont identiques : {pred1_text}"
    print("SUCCESS: 0 exception et deux prédictions distinctes validées !")

if __name__ == "__main__":
    test_regression_doc1_app()
