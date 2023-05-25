import psycopg2
from django import forms
from django.db import connection


# def get_database():
#     conn = psycopg2.connect(database="tk3_sepakbola", user="postgres", password="postgres")
#     return conn


# def get_stadiums():
#     with get_database().cursor() as cursor:
#         cursor.execute('SELECT id_stadium, nama FROM Stadium')
#         list_stadium = cursor.fetchall()
#         return list_stadium


# class StadiumForm(forms.Form):
#     stadium = forms.ChoiceField(choices=get_stadiums())
#     tanggal = forms.DateField(widget=forms.SelectDateWidget)


# class PembayaranForm(forms.Form):
#     jenis_tiket = forms.ChoiceField(choices=[('VIP', 'VIP'), ('Main East', 'Main East'), ('Kategori 1', 'Kategori 1'),
#                                              ('Kategori 2', 'Kategori 2')])
#     pembayaran = forms.ChoiceField(
#         choices=[('ShopeePay', 'ShopeePay'), ('Gopay', 'Gopay'), ('Bank', 'Bank'), ('Ovo', 'Ovo')])
