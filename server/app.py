import os

from flask import Flask, render_template
from supabase import create_client

url = 'https://tpgbsatkplqmdglpiuyz.supabase.co/'
key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRwZ2JzYXRrcGxxbWRnbHBpdXl6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDEyODU1NzAsImV4cCI6MjA1Njg2MTU3MH0.EvTW2Ktpqtl3FANUTT7Q3z_v-oYQN1kU-83PnF0AvPo'
supabase = create_client(url, key)

response = supabase.table("parties").select("*").execute()
print(response)

'''app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)'''
