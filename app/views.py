"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file contains the routes for your application.
"""
import os
from app import app, db
from flask import render_template, request, redirect, url_for, flash, session, send_from_directory
from werkzeug.utils import secure_filename
from app.models import Property
from app.forms import PropertyForm


###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html', name="Mary Jane")

@app.route('/properties/create',methods=['GET','POST'])
def create_property():
    pform = PropertyForm()
    
    if pform.validate_on_submit():
        if 'photo' in request.files:
            file = request.files['photo']
            if file:
                fname = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'],fname))
                
                prop = {
                'title':pform.title.data,
                'description':pform.description.data,
                'bedrooms':pform.bedrooms.data,
                'bathrooms':pform.bathrooms.data,
                'price':pform.price.data,
                'type':pform.type.data,
                'location':pform.location.data,
                'photo':fname,
                }
                
                newprop = Property(**prop)
                db.session.add(newprop)
                db.session.commit()
        
                
                flash('Property successfully added!','success')
                return redirect(url_for('display_properties'))
            else:
                flash('Error!','error')
        else:
            flash('Error2!','error')
                
    return render_template('create_property.html',form=pform)

@app.route('/properties',methods=['GET'])
def display_properties():
    prop = Property.query.all()
    return render_template('properties.html',properties=prop)

@app.route('/properties/<int:propertyid>',methods=['GET'])
def view_property(propertyid):
    prop = Property.query.get_or_404(propertyid)
    return render_template('view_property.html',propertyid=propertyid,property=prop)
    
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    root_dir = os.getcwd()
    ufldr = app.config["UPLOAD_FOLDER"]
    return send_from_directory(os.path.join(root_dir,ufldr),filename)
###
# The functions below should be applicable to all Flask apps.
###

# Display Flask WTF errors as Flash messages
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'danger')

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404
