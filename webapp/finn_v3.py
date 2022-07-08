from os import stat, times
from typing import List
import requests
from bs4 import BeautifulSoup
# import mysql.connector
import datetime
import requests
import sys
from .models import Listing, Price_History


class FinnScraper:

    def new_data_today(self):
        print("Starting Today Data")

        for i in range(10):
            print("Page No. {}".format(i+1))
            url = "https://www.finn.no/boat/forsale/search.html?filters=&page={}&published=1".format(
                i+1)
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            error_found = soup.select_one("#__next h1")
            no_hits_error = soup.select_one("h3.u-pa16.u-text-center")
            if error_found is not None:
                error_found = error_found.text
            else:
                error_found = "Empty"

            if no_hits_error is not None:
                no_hits_error = no_hits_error.text
            else:
                no_hits_error = "Empty"

            if "Beklager, nå er det rusk i maskineriet" in error_found:
                break
            elif "Ingen treff akkurat nå" in no_hits_error:
                break
            else:
                links = soup.find_all("a", {"class": "ads__unit__link"})
                for link in links:
                    if "www.finn.no" not in link["href"]:
                        pass
                    else:
                        try:
                            self.scrape_single_listing(link['href'])
                        except:
                            pass
    def old_data(self):
        print("Starting Old Data scraping")
        for i in range(50):
            print("Page No. {}".format(i+1))
            url = "https://www.finn.no/boat/forsale/search.html?page={}&sort=YEAR_DESC".format(i+1)
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            error_found = soup.select_one("#__next h1")
            no_hits_error = soup.select_one("h3.u-pa16.u-text-center")
            if error_found is not None:
                error_found = error_found.text
            else:
                error_found = "Empty"

            if no_hits_error is not None:
                no_hits_error = no_hits_error.text
            else:
                no_hits_error = "Empty"

            if "Beklager, nå er det rusk i maskineriet" in error_found:
                break
            elif "Ingen treff akkurat nå" in no_hits_error:
                break
            else:
                links = soup.find_all("a", {"class": "ads__unit__link"})
                for link in links:
                    if "www.finn.no" not in link["href"]:
                        pass
                    else:
                        try:
                            self.scrape_single_listing(link['href'])
                        except:
                            pass

    def scrape_single_listing(self, url):
        print("Scraping: ", url)
        timestamp = str(datetime.datetime.now())[:-7]
        response = requests.get(url+"&showContactInfo=true").text
        soup = BeautifulSoup(response, 'html.parser')
        title = soup.select_one("h1.u-word-break.u-t2").text
        price = str(soup.select_one("span.u-t3").text).replace("kr","").replace(" ", "").replace(u'\xa0', "")
        status = soup.select_one("span.status")
        if status:
            if "SOLGT" in status:
                status = "Sold"
            elif "Utløpt" in status:
                status = "Expired"
            else:
                status = status.text
        else:
            status = "Active"
        # print(price)
        # --------------------------------------------------------------------------------------------------------------------------------
        # Definitions List Parsing Start
        definition_list = soup.select_one(
            "dl.definition-list.definition-list--cols1to2")
        keys = definition_list.find_all('dt')
        values = definition_list.find_all('dd')
        Boat_location = ""
        State = ""
        Type = ""
        Brand = ""
        Model = ""
        Model_Year = ""
        Length_cm = ""
        Length_feet = ""
        Width = ""
        Depth = ""
        Engine_Included = ""
        Engine_Manufacturer = ""
        Engine_Type = ""
        Motorstr = ""
        Max_Speed = ""
        Fuel = ""
        Weight = ""
        Material = ""
        Color = ""
        Seating = ""
        Sleeps = ""
        for key, value in zip(keys, values):
            if "Båten står i" in key:
                Boat_location = value.text
            if "Tilstand" in key:
                State = value.text
            if "Type" in key:
                Type = value.text
            if "Merke" in key:
                Brand = value.text
            if "Modell" in key:
                Model = value.text
            if "Årsmodell" in key:
                Model_Year = value.text
            if "Lengde i fot" in key:
                Length_feet = value.text
            if "Lengde i cm" in key:
                Length_cm = value.text
            if "Bredde" in key:
                Width = value.text
            if "Dybde" in key:
                Depth = value.text
            if "Motor Inkl." in key:
                Engine_Included = value.text
            if "Motorfabrikant" in key:
                Engine_Manufacturer = value.text
            if "Motortype" in key:
                Engine_Type = value.text
            if "Motorstr." in key:
                Motorstr = value.text
            if "Maks fart" in key:
                Max_Speed = value.text
            if "Drivstoff" in key:
                Fuel = value.text
            if "Vekt" in key:
                Weight = value.text
            if "Materiale" in key:
                Material = value.text
            if "Farge" in key:
                Color = value.text
            if "Sitteplasser" in key:
                Seating = value.text
            if "Soveplasser" in key:
                Sleeps = value.text
        # Definition List parsing End
        # --------------------------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------------------------
        descriptions = soup.select(".panel.import-decoration")
        description = ""
        for item in descriptions:
            # description =  description + str("\n"+item.text).replace("        ","")
            description = description + str(item).strip()
        # --------------------------------------------------------------------------------------------------------------------------------

        # Add Info----------------
        ad_info = soup.select_one(".panel.u-text-left")
        info_list = ad_info.find_all("td")
        finn_kode = str(info_list[0].text).replace("\n", "")
        last_changed = str(info_list[1].text).replace("\n", "")
        # Add Info----------------

        side_panel = soup.select_one("dl.definition-list.u-mt16")
        info_summary = soup.select_one("div.identity__summary__body")
        extended_profile_panel = soup.select_one(
            "div.panel.extended-profile-container")
        if side_panel:
            contact_information = side_panel.select("dd")

            contact_name = contact_information[0].text
            try:
                phone_number = str(contact_information[-1].find("a")["href"]).replace("tel:", "")
            except:
                phone_number = ""
        elif info_summary:
            if "Du må være logget inn for å se profilen" in info_summary.text:
                contact_name = ""
                phone_number = ""
            else:
                info_summary = soup.select_one("div.identity__summary__body")
                contact_name = info_summary.find('a').text
                phone_number = ""

        elif extended_profile_panel:
            contact_div = extended_profile_panel.select_one("div.contact")
            contact_name = contact_div.select_one("h3.name")
            phone_numbers_div = contact_div.select_one("ul.ul-bordered.mhn")
            phone_numbers_list = phone_numbers_div.select("li")

            phone_number = ""
            for number in phone_numbers_list:
                phone = str(number.find("a")["href"])
                if "tel:" in phone:
                    phone_number = phone_number + "\n" + phone

            phone_number = phone_number.replace("tel:", "")

            if contact_name is not None:
                contact_name = contact_name.text
            else:
                contact_name = ""

            if phone_number is not None:
                phone_number = phone_number
            else:
                phone_number = ""
        try:
            address_side_panel_1 = soup.select_one(
                "body > main > div > div.grid > div.grid__unit.u-r-size1of3 > section:nth-child(4)")
            address_side_panel_2 = soup.select_one(
                "body > main > div > div.grid > div.grid__unit.u-r-size1of3 > section")
            address_side_panel_3 = "body > main > div > div.grid > div.grid__unit.u-r-size1of3 > section:nth-child(3)"
            if address_side_panel_1 is not None:
                address = address_side_panel_1.select_one('h2.u-t3').text
            else:
                address = ""
            if address_side_panel_2 is not None:
                if "Kontakt" not in address_side_panel_2:
                    address = address_side_panel_2.select_one('h2.u-t3').text
                    
            else:
                address = ""
            if address_side_panel_3 is not None:
                address = address_side_panel_1.select_one('h2.u-t3').text
            else:
                address = ""
        except:
            address = ""

        image = soup.select_one(
            "img.img-format__img.u-border-radius-8px")
        if image:
            image = image["src"]
        else:
            image = "https://static.finncdn.no/_c/mfinn/static/images/no-image-text.642b3397.svg"

        if self.check_duplicate(finn_kode):

            object_data = Listing.objects.get(finn_code=finn_kode)
            object_data.status = status
            object_data.lastupdated = timestamp
            object_data.save()

            if self.check_price(finn_kode, price):
                print("Price is Same")
                pass
            else:
                print("Price is Changed")
                if Price_History.objects.filter(finn_code=finn_kode, changed_price=price).exists():
                    pass
                else:
                    object_data = Price_History.objects.create(
                        finn_code=finn_kode, changed_price=price, price_changed_date=last_changed)
                    object_data.price = price
                    object_data.save()

        else:
            print("Not Exist")
            inputdata = Listing.objects.create(finn_code=finn_kode, title=str(title), description=str(description).replace("<p><br/></p>", "").replace("<br/><br/>", "<br/>").replace("<p><b>&nbsp;</b></p>", "").replace("<b>", "").replace("</b>", ""), definitions_html=str(definition_list), Boat_location=str(Boat_location), State=str(State), Type=str(Type), Brand=str(Brand), Model=str(Model), Model_Year=str(Model_Year), Length_feet=str(Length_feet), Length_cm=str(Length_cm), Width=str(Width), Depth=str(Depth), Engine_Included=str(Engine_Included), Engine_Manufacturer=str(
                Engine_Manufacturer), Engine_Type=str(Engine_Type), Motorstr=str(Motorstr), Max_Speed=str(Max_Speed), Fuel=str(Fuel), Weight=str(Weight), Material=str(Material), Color=str(Color), Seating=str(Seating), Sleeps=str(Sleeps), orignal_price=str(price), last_changed=str(last_changed), contact_name=str(contact_name), phone_number=str(phone_number), address=str(address), image=str(image), last_updated=str(timestamp), url=str(url), status=str(status))

            inputdata.save()
            print("Data Saved\n")

    def check_price(self, finn_code, price):

        try:
            data_check = Listing.objects.get(finn_code=finn_code)
            price_check = data_check.orignal_price
        except:
            price_check = ""
        if price == str(price_check):
            return True
        else:
            return False

    def check_duplicate(self, finn_code):
        try:
            data_check = Listing.objects.get(finn_code=finn_code)
        except:
            data_check = ""
        if str(finn_code) in str(data_check):
            return True
        else:
            return False
