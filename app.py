from flask import Flask, render_template, request
from recommend import recommend_restaurants, df_encoded

app = Flask(__name__)

locations = [col.replace('location_', '') for col in df_encoded.columns if col.startswith('location_')]
locations.sort()

cuisines = [col for col in df_encoded.columns
            if col not in ['name', 'rate', 'votes', 'cost_for_two', 'online_order', 'book_table']
            and not col.startswith('location_')
            and not col.startswith('rest_type_')]
cuisines.sort()

@app.route('/', methods=['GET', 'POST'])
def home():
    recommendations, message = [], ""
    if request.method == 'POST':
        location = request.form.get('location')
        online_order = int(request.form.get('online_order'))
        book_table = int(request.form.get('book_table'))
        selected_cuisines = request.form.getlist('cuisines')
        
        recommendations = recommend_restaurants(location, online_order, book_table, selected_cuisines)
        if not recommendations:
            message = "No matching restaurants found."
    
    return render_template('index.html', locations=locations, cuisines=cuisines, recommendations=recommendations, message=message)

if __name__ == '__main__':
    app.run(debug=True,host = "0.0.0.0",port = 5000)
