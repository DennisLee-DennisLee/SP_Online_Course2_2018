#!/usr/bin/env python3

from mailroom import Donor, Donors, donors, quit_menu

import os

def test_quit_menu():
    assert quit_menu() == 'Quit'

def test_list_donors():
    assert donors.list_donors().strip() == "---------- Donors ----------\nBill Ted\nFrank Fred\nLaura Todd\nSteve Lincoln\nLisa Grant"

def test_find_donor():
    assert donors.find_donor("dne") is None
    assert donors.find_donor("Bill Ted") == Donor("Bill Ted", [353.53, 348.1, 25.00])

def test_total_donations():
    donor = donors.find_donor("Lisa Grant")
    assert donor.total_donations == 209.70
    donor = donors.find_donor("Frank Fred")
    assert donor.total_donations == 178.76

def test_avg_donations():
    donor = donors.find_donor("Lisa Grant")
    assert donor.avg_donation == 104.85
    donor = donors.find_donor("Bill Ted")
    assert donor.avg_donation == 242.21

def test_num_donations():
    donor = donors.find_donor("Lisa Grant")
    assert donor.num_donations == 2
    donor = donors.find_donor("Frank Fred")
    assert donor.num_donations == 3

def test_name():
    donor = donors.find_donor("Lisa Grant")
    assert donor.name == "Lisa Grant"
    donor = donors.find_donor("Frank Fred")
    assert donor.name == "Frank Fred"

def test_donor_lt():
    donor1 = Donor("A", [5, 5])
    donor2 = Donor("B", [4, 10])
    assert donor1 < donor2
    donor2 = Donor("B", [7, 1])
    assert donor1 > donor2

def test_donor_eq():
    donor1 = Donor("A", [5, 5])
    donor2 = Donor("B", [4, 10])
    assert not (donor1 == donor2)
    donor2 = Donor("A", [5, 5])
    assert donor1 == donor2

def test_mail_everyone():
    donors.mail_everyone()
    dir_files = os.listdir()
    assert 'bill_ted.txt' in dir_files
    assert 'frank_fred.txt' in dir_files
    assert 'laura_todd.txt' in dir_files
    assert 'steve_lincoln.txt' in dir_files
    assert 'lisa_grant.txt' in dir_files

    with open('bill_ted.txt') as in_file:
        file_contents = in_file.read()
        assert file_contents.strip() == ("Dear Bill Ted,\nThank you for your very generous donation of $726.63.  "
            "It \nwill go very far in supporting the Human Fund, \"Money for \nPeople.\"\n"
            "                               Sincerely\n                                      Art Vandelay")

def test_create_report():
    assert donors.create_report().strip() == (
        "Donor Name          | Total Given | Num Gifts | Average Gift\n"
        "-------------------------------------------------------------\n"
        "Bill Ted            | $    726.63 |         3 | $     242.21\n"
        "Lisa Grant          | $    209.70 |         2 | $     104.85\n"
        "Frank Fred          | $    178.76 |         3 | $      59.59\n"
        "Steve Lincoln       | $    165.28 |         2 | $      82.64\n"
        "Laura Todd          | $      5.75 |         1 | $       5.75"
        )

def test_create_thank_you():
    donor = donors.find_donor("Bill Ted")
    assert donor.create_thank_you(5) == ("Dear Bill Ted,\nThank you for your very generous donation of $5.00.  "
        "It \nwill go very far in supporting the Human Fund, \"Money for \nPeople.\"\n"
        "                               Sincerely\n                                      Art Vandelay")

def test_add_donation():
    assert donors.add_donation("Test1", 55.55) == Donor("Test1", [55.55])
    assert donors.add_donation("Test1", 4) == Donor("Test1", [55.55, 4])
    assert donors.add_donation("Laura Todd", 99) == Donor("Laura Todd", [5.75, 99])

def test_load():
    donors.load("test_donors.json")
    donor = donors.find_donor("Bill Ted")
    assert donor is None
    donor = donors.find_donor("Json Donor 1")
    donor2 = Donor("Json Donor 1", [4.50, 3.45])
    assert donor == donor2

def test_save():
    donors.load("test_donors.json")
    donors.add_donor( Donor("Json Donor 2", [5.50, 5.45]))
    donors.save("test_donors_save.json")
    donors.load("test_donors.json")
    donor = donors.find_donor("Json Donor 2")
    assert donor is None
    donors.load("test_donors_save.json")
    donor = donors.find_donor("Json Donor 2")
    donor2 = Donor("Json Donor 2", [5.50, 5.45])
    assert donor == donor2


