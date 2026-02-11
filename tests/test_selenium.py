import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import smtplib
from email.mime.text import MIMEText


# chrome
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

# firefox
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service as FirefoxService

import os

class TestCalculator:

    @pytest.fixture(scope="class")
    def driver(self):

        """Configuration du driver Chrome pour les tests"""
        chrome_options = Options()
        # Configuration pour environnement CI/CD
        if os.getenv('CI'):
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--window-size=1920,1080')
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.implicitly_wait(10)
        yield driver
        driver.quit()

    def driver_firefox(self):
        """Configuration du driver Firefox pour les tests"""
        firefox_options = FirefoxOptions()
        # Configuration pour environnement CI/CD
        if os.getenv('CI'):
            firefox_options.add_argument('--headless')
            firefox_options.add_argument('--no-sandbox')
            firefox_options.add_argument('--disable-dev-shm-usage')
            firefox_options.add_argument('--disable-gpu')
            firefox_options.add_argument('--window-size=1920,1080')
        service = FirefoxService(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=firefox_options)
        driver.implicitly_wait(10)
        return driver



    def test_page_loads(self, driver):
        """Test 1: Vérifier que la page se charge correctement"""
        file_path = os.path.abspath("../src/index.html")
        driver.get(f"file://{file_path}")

        # Vérifier le titre
        assert "Calculatrice Simple" in driver.title

        # Vérifier la présence des éléments principaux
        assert driver.find_element(By.ID, "num1").is_displayed()
        assert driver.find_element(By.ID, "num2").is_displayed()
        assert driver.find_element(By.ID, "operation").is_displayed()
        assert driver.find_element(By.ID, "calculate").is_displayed()

    def test_addition(self, driver):
        """Test 2: Tester l'addition"""
        file_path = os.path.abspath("../src/index.html")
        driver.get(f"file://{file_path}")

        # Saisir les valeurs
        driver.find_element(By.ID, "num1").send_keys("10")
        driver.find_element(By.ID, "num2").send_keys("5")
        # Sélectionner l'addition

        select = Select(driver.find_element(By.ID, "operation"))
        select.select_by_value("add")
        # Cliquer sur calculer

        driver.find_element(By.ID, "calculate").click()
        # Vérifier le résultat

        result = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "result"))
        )
        assert "Résultat: 15" in result.text

    def test_division_by_zero(self, driver):
        """Test 3: Tester la division par zéro"""
        file_path = os.path.abspath("../src/index.html")
        driver.get(f"file://{file_path}")
        # Saisir les valeurs
        driver.find_element(By.ID, "num1").clear()
        driver.find_element(By.ID, "num1").send_keys("10")
        driver.find_element(By.ID, "num2").clear()
        driver.find_element(By.ID, "num2").send_keys("0")
        # Sélectionner la division
        select = Select(driver.find_element(By.ID, "operation"))
        select.select_by_value("divide")
        driver.find_element(By.ID, "calculate").click()
        # Vérifier le message d'erreur
        result = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "result"))
        )
        assert "Erreur: Division par zéro" in result.text

    def test_all_operations(self, driver):
        """Test 4: Tester toutes les opérations"""
        file_path = os.path.abspath("../src/index.html")
        driver.get(f"file://{file_path}")
        operations = [
            ("add", "8", "2", "10"),
            ("subtract", "8", "2", "6"),
            ("multiply", "8", "2", "16"),
            ("divide", "8", "2", "4")
        ]
        for op, num1, num2, expected in operations:

            # Nettoyer les champs
            driver.find_element(By.ID, "num1").clear()
            driver.find_element(By.ID, "num2").clear()

            # Saisir les valeurs
            driver.find_element(By.ID, "num1").send_keys(num1)
            driver.find_element(By.ID, "num2").send_keys(num2)

            # Sélectionner l'opération
            select = Select(driver.find_element(By.ID, "operation"))
            select.select_by_value(op)

            # Calculer
            driver.find_element(By.ID, "calculate").click()

            # Vérifier le résultat
            result = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "result"))
            )

            assert f"Résultat: {expected}" in result.text
            time.sleep(1)

    def test_page_load_time(self, driver):
        """Test 5: Mesurer le temps de chargement de la page"""
        start_time = time.time()
        file_path = os.path.abspath("../src/index.html")
        driver.get(f"file://{file_path}")
        # Attendre que la page soit complètement chargée
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "calculator"))
        )
        load_time = time.time() - start_time
        print(f"Temps de chargement: {load_time:.2f} secondes")
        # Vérifier que le chargement prend moins de 3 secondes
        assert load_time < 3.0, f"Page trop lente à charger: {load_time:.2f}s"

    def test_negativ_value(self, driver):
        """Test 6: Tester les valeurs négatives"""
        file_path = os.path.abspath("../src/index.html")
        driver.get(f"file://{file_path}")
        # Saisir les valeurs
        driver.find_element(By.ID, "num1").clear()
        driver.find_element(By.ID, "num1").send_keys("-5")
        driver.find_element(By.ID, "num2").clear()
        driver.find_element(By.ID, "num2").send_keys("-3")
        # Sélectionner l'addition
        select = Select(driver.find_element(By.ID, "operation"))
        select.select_by_value("add")
        # Cliquer sur calculer
        driver.find_element(By.ID, "calculate").click()
        # Vérifier le résultat
        result = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "result"))
        )
        assert "Résultat: -8" in result.text

    def test_decimal_number(self, driver):
        """test 7: Tester les nombres décimaux"""
        file_path = os.path.abspath("../src/index.html")
        driver.get(f"file://{file_path}")
        # Saisir les valeurs
        driver.find_element(By.ID, "num1").clear()
        driver.find_element(By.ID, "num1").send_keys("5.5")
        driver.find_element(By.ID, "num2").clear()
        driver.find_element(By.ID, "num2").send_keys("2.3")
        # Sélectionner la multiplication
        select = Select(driver.find_element(By.ID, "operation"))
        select.select_by_value("multiply")
        # Cliquer sur calculer
        driver.find_element(By.ID, "calculate").click()
        # Vérifier le résultat
        result = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "result"))
        )
        assert "Résultat: 12.65" in result.text
    
    def test_UI(self, driver):
        """Test 8: Vérifier l'interface utilisateur"""
        file_path = os.path.abspath("../src/index.html")
        driver.get(f"file://{file_path}")
        # Vérifier la présence du titre
        assert driver.find_element(By.TAG_NAME, "h1").is_displayed()
        # Vérifier les labels
        assert driver.find_element(By.XPATH, "//label[@for='num1']").is_displayed()
        assert driver.find_element(By.XPATH, "//label[@for='num2']").is_displayed()
        assert driver.find_element(By.XPATH, "//label[@for='operation']").is_displayed()
        # Vérifier le bouton
        assert driver.find_element(By.ID, "calculate").is_displayed()
        # Vérifier les couleurs et les styles
        assert driver.find_element(By.ID, "calculate").value_of_css_property("background-color") == "rgba(0, 123, 255, 1)"  # Couleur du bouton
        assert driver.find_element(By.ID, "calculate").value_of_css_property("color") == "rgba(255, 255, 255, 1)"  # Couleur du texte du bouton

if __name__ == "__main__":
    pytest.main(["-v", "--html=report.html", "--self-contained-html"])
    # send the report by mail in case of errors :

    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        sender = "your email"
        sender_password = "your email password"
        receiver = "who you want to send email to"

        smtp.login(sender, sender_password)
        subject = 'Tickets Were Found!'
        body = "What you want to say about the tickets"
        message = f'Subject: {subject}\n\n{body}'

        smtp.sendmail(sender, receiver, message)
        print("Email sent!")

# source : https://stackoverflow.com/questions/62515478/selenium-python-is-there-some-way-to-send-out-an-e-mail-or-sms-if-a-certain-eve
# source : https://www.selenium.dev/documentation/webdriver/waits/explicit_waits/
# source : https://www.selenium.dev/documentation/webdriver/interactions/select_elements/
