from flask import Flask, render_template, request, redirect, send_file, make_response
from PIL import Image
import io

app = Flask(__name__)

# Function to overlay the logo on the user's image
def overlay_logo(user_image, microsoft_logo, opacity=0.85):
    user_image = Image.open(user_image).convert("RGBA")
    microsoft_logo = Image.open(microsoft_logo).convert("RGBA")

    user_width, user_height = user_image.size
    logo_width, logo_height = microsoft_logo.size
    aspect_ratio = user_height / logo_height

    new_logo_width = int(logo_width * aspect_ratio)
    new_logo_height = user_height
    microsoft_logo = microsoft_logo.resize((new_logo_width, new_logo_height))

    x_position = 0
    y_position = 0

    canvas = Image.new("RGBA", user_image.size, (0, 0, 0, 0))

    for x in range(new_logo_width):
        for y in range(new_logo_height):
            r, g, b, a = microsoft_logo.getpixel((x, y))
            canvas.putpixel((x + x_position, y + y_position), (r, g, b, int(a * opacity)))

    result_image = Image.alpha_composite(user_image, canvas)

    # Create an in-memory file object to store the result image
    result_io = io.BytesIO()
    result_image.save(result_io, format='PNG')
    result_io.seek(0)

    return result_io

# List of available Microsoft logo options
microsoft_logos = {

    "RC Pakistan": "static/RCPakistan.png",
    "RC Saudi Arabia": "static/RCSaudia.png",
    "RC India": "static/RCIndia.png",
    "RC USA": "static/RCUSA.png",
    "RC Australia": "static/RCAustralia.png",
    "RC Canada": "static/RCCanada.png",
    "RC Mexico": "static/RCMexico.png",
    "RC New Zealand": "static/RCNewZealand.png",
    "RC South Africa": "static/RCSouthAfrica.png",
    "RC UK": "static/RCUk.png"

}

# Route for the homepage with the file upload form
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        user_image = request.files['user_image']
        if user_image and user_image.filename != '':
            selected_logo = request.form['logo_choice']  # Get the selected logo from the form
            
            if selected_logo in microsoft_logos:
                microsoft_logo_path = microsoft_logos[selected_logo]  # Get the path of the selected logo
                result_io = overlay_logo(user_image, microsoft_logo_path)
                
                # Create a response with the image to display to the user
                response = make_response(send_file(result_io, mimetype='image/png'))
                
                # Set content disposition to inline to display the image in the browser
                response.headers['Content-Disposition'] = 'inline; filename=result_image.png'
                
                return response
    return render_template('index.html', microsoft_logos=microsoft_logos)

if __name__ == '__main__':
    app.run(debug=True)
