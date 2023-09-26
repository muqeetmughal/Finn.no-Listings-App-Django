import requests
from bs4 import BeautifulSoup
import datetime
from django.conf import settings
import os
from django.db import close_old_connections

# os.environ["DJANGO_SETTINGS_MODULE"] = "finn.settings"
# django.setup()

from webapp.models import Listing, Price_History


def convert_string_to_datetime(date_string):
    try:
        date_format = "%d. %b %Y %H:%M"

        datetime_obj = datetime.datetime.strptime(date_string, date_format)
        return datetime_obj
    except:
        return None


class FinnScraper:
    def __init__(self):
        self.base_url = "https://www.finn.no"
        self.session = requests.Session()

    def check_price(self, finn_code, price):
        try:
            listing = Listing.objects.get(finn_code=finn_code)
            price_check = listing.orignal_price
        except:
            price_check = ""
        if price == str(price_check):
            return True
        else:
            return False

    def check_duplicate(self, finn_code):
        try:
            listing = Listing.objects.get(finn_code=finn_code)
        except:
            listing = ""
        if str(finn_code) in str(listing):
            return True
        else:
            return False

    def scrape_data(self, old=False):
        if old:
            print("Scraping Old Data")

            url = "https://www.finn.no/boat/forsale/search.html?page={}&sort=YEAR_ASC"
        else:
            print("Scraping New Data")
            url = "https://www.finn.no/boat/forsale/search.html?page={}&published=1&sort=PUBLISHED_DESC"

        page = 1
        while True:
            print("Page No. {}".format(url.format(page)))
            response = self.session.get(url.format(page))
            soup = BeautifulSoup(response.text, "html.parser")
            links = soup.select("a.sf-search-ad-link.link")
            error_found = soup.select_one("#__next h1")

            if error_found and not links:
                break

            for link in links:
                try:
                    if "www.finn.no" not in link.get("href"):
                        link = self.base_url + link.get("href")
                    else:
                        link = link.get("href")
                    try:
                        self.scrape_single_listing(link)
                    except Exception as e:
                        print("Failed to scrape Single listing", link, e)
                        continue

                except Exception as e:
                    print("Something went wrong for Single listing", link, e)
            page = page + 1

    def scrape_single_listing(self, url):
        print("Scraping: ", url)
        timestamp = str(datetime.datetime.now())[:-7]
        print("time stamp is : ", timestamp)
        try:
            response = self.session.get(url + "&showContactInfo=true").text
            soup = BeautifulSoup(response, "html.parser")
            title = soup.select_one("h1.u-word-break.u-t2").text
            price = int(
                str(soup.select_one("span.u-t3").text)
                .replace("kr", "")
                .replace(" ", "")
                .replace("\n", "")
                .replace("\xa0", "")
            )
            status = soup.select_one("span.status")
            if status:
                if "SOLGT" in status:
                    status = "Sold"
                elif "Utløpt" in status:
                    status = "Expired"
                else:
                    status = str(status.text).strip().replace("\n", "")
            else:
                status = None

            definition_list = soup.select_one(
                "dl.definition-list.definition-list--cols1to2"
            )
            keys = definition_list.find_all("dt")
            values = definition_list.find_all("dd")
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
                description = description + str(item.text).strip() + "\n"
            # --------------------------------------------------------------------------------------------------------------------------------

            # Add Info----------------
            ad_info = soup.select_one(".panel.u-text-left")
            info_list = ad_info.find_all("td")
            finn_kode = str(info_list[0].text).replace("\n", "")
            last_changed = str(info_list[1].text).replace("\n", "")
            # last_changed = last_changed.replace(".","").split()

            # print("Last Created",last_changed)

            # datetime.datetime(int(last_changed[0]), 2, 3, 6, 30, 15, 0, pytz.timezone('Pacific/Johnston'))
            # Add Info----------------

            side_panel = soup.select_one("dl.definition-list.u-mt16")  # not working
            info_summary = soup.select_one(
                "div.identity__summary__body"
            )  # not working mostly all of below in panels
            extended_profile_panel = soup.select_one(
                "div.panel.extended-profile-container"
            )
            if side_panel:
                contact_information = side_panel.select("dd")

                contact_name = contact_information[0].text
                try:
                    phone_number = str(
                        contact_information[-1].find("a")["href"]
                    ).replace("tel:", "")
                except:
                    phone_number = ""
            elif info_summary:
                if "Du må være logget inn for å se profilen" in info_summary.text:
                    contact_name = ""
                    phone_number = ""
                else:
                    info_summary = soup.select_one("div.identity__summary__body")
                    contact_name = info_summary.find("a").text
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
                    "body > main > div > div.grid > div.grid__unit.u-r-size1of3 > section:nth-child(4)"
                )
                address_side_panel_2 = soup.select_one(
                    "body > main > div > div.grid > div.grid__unit.u-r-size1of3 > section"
                )
                address_side_panel_3 = "body > main > div > div.grid > div.grid__unit.u-r-size1of3 > section:nth-child(3)"
                if address_side_panel_1 is not None:
                    address = address_side_panel_1.select_one("h2.u-t3").text
                else:
                    address = ""
                if address_side_panel_2 is not None:
                    if "Kontakt" not in address_side_panel_2:
                        address = address_side_panel_2.select_one("h2.u-t3").text

                else:
                    address = ""
                if address_side_panel_3 is not None:
                    address = address_side_panel_1.select_one("h2.u-t3").text
                else:
                    address = ""
            except:
                address = ""

            image = soup.select_one("img.img-format__img.u-border-radius-8px")
            if image:
                image = image["src"]
            else:
                image = "https://static.finncdn.no/_c/mfinn/static/images/no-image-text.642b3397.svg"

            # data = {
            #     "finn_code": int(finn_kode),
            #     "title": str(title),
            #     "description": str(description)
            #     .replace("<p><br/></p>", "")
            #     .replace("<br/><br/>", "<br/>")
            #     .replace("<p><b>&nbsp;</b></p>", "")
            #     .replace("<b>", "")
            #     .replace("</b>", ""),
            #     "definitions_html": str(definition_list),
            #     "Boat_location": str(Boat_location),
            #     "State": str(State),
            #     "Type": str(Type),
            #     "Brand": str(Brand),
            #     "Model": str(Model),
            #     "Model_Year": str(Model_Year),
            #     "Length_feet": str(Length_feet),
            #     "Length_cm": str(Length_cm),
            #     "Width": str(Width),
            #     "Depth": str(Depth),
            #     "Engine_Included": str(Engine_Included),
            #     "Engine_Manufacturer": str(Engine_Manufacturer),
            #     "Engine_Type": str(Engine_Type),
            #     "Motorstr": str(Motorstr),
            #     "Max_Speed": str(Max_Speed),
            #     "Fuel": str(Fuel),
            #     "Weight": str(Weight),
            #     "Material": str(Material),
            #     "Color": str(Color),
            #     "Seating": str(Seating),
            #     "Sleeps": str(Sleeps),
            #     "orignal_price": str(price),
            #     "last_changed": str(last_changed),
            #     "contact_name": str(contact_name),
            #     "phone_number": str(phone_number),
            #     "address": str(address),
            #     "image": str(image),
            #     "last_updated": str(timestamp),
            #     "url": str(url),
            #     "status": str(status),
            # }
            # # print(data)

            try:
                listing = Listing.objects.get(finn_code=int(finn_kode))
                print("[", listing, "]  Already Exist Updating it...")

                listing.status = status
                listing.last_updated = timestamp
                listing.save()

                if int(price) != int(listing.orignal_price):
                    if not Price_History.objects.filter(
                        listing=finn_kode,
                        # price_changed_date=last_changed,
                        # last_changed_datetime=convert_string_to_datetime(last_changed),
                        changed_price=price,
                    ).exists():
                        print("Price Changed Now Updating...")
                        Price_History.objects.create(
                            changed_price=price,
                            price_changed_date=last_changed,
                            listing=listing,
                            last_changed_datetime=convert_string_to_datetime(
                                last_changed
                            ),
                        )

            except Listing.DoesNotExist:
                print("Result is NOne add Entry")
                Listing.objects.create(
                    finn_code=int(finn_kode),
                    title=str(title),
                    description=str(description),
                    Boat_location=str(Boat_location),
                    State=str(State),
                    Type=str(Type),
                    Brand=str(Brand),
                    Model=str(Model),
                    Model_Year=str(Model_Year),
                    Length_feet=str(Length_feet),
                    Length_cm=str(Length_cm),
                    Width=str(Width),
                    Depth=str(Depth),
                    Engine_Included=str(Engine_Included),
                    Engine_Manufacturer=str(Engine_Manufacturer),
                    Engine_Type=str(Engine_Type),
                    Motorstr=str(Motorstr),
                    Max_Speed=str(Max_Speed),
                    Fuel=str(Fuel),
                    Weight=str(Weight),
                    Material=str(Material),
                    Color=str(Color),
                    Seating=str(Seating),
                    Sleeps=str(Sleeps),
                    orignal_price=int(price),
                    last_changed=str(last_changed),
                    last_changed_datetime=convert_string_to_datetime(last_changed),
                    contact_name=str(contact_name),
                    phone_number=str(phone_number),
                    address=str(address),
                    image=str(image),
                    last_updated=str(timestamp),
                    url=str(url),
                    status=str(status),
                )

        except Exception as e:
            print(e)


if __name__ == "__main__":
    finn = FinnScraper()
    # finn.scrape_single_listing("https://www.finn.no/boat/forsale/ad.html?finnkode=263049309")
    finn.scrape_data()
    close_old_connections()
