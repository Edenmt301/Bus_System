from collections import defaultdict
from turtle import distance
from flask import Flask, jsonify,  request, Blueprint,render_template, flash , redirect , url_for , request
from busSystem import app,db,pwd
from busSystem.forms import LoginForm
from flask_login import login_user , current_user , logout_user , login_required
from busSystem.models import Route, User, Bus, Station, Route_Station
import random

def policy(method, station_names,bus_id):
    if method == 1:
        #preassigned
        bus = Bus.query.get(bus_id)
        route = Route.query.get(bus.route_id)
        response = {
         'status': 'success',
               }
        response['route_id'] = route.id
        response['route_name'] = route.name
        return jsonify(response), 201
    elif method == 2:
        station = Station.query.filter_by(name=station_names).first()
        if station:
            routes = Route.query.filter_by(starting_station=station.id).all()
            counts = defaultdict(int)
            current_counts = Route_Station.query.all()
            for each in routes:
                counts[each.id] = 0
            for each in current_counts:
                if each.route_id in counts:
                    counts[each.route_id] += each.count
            current_bus = bus.query.get(bus_id)
            max_count, max_route = 0, 1
            for key in counts:
                if counts[key] > max_count:
                    max_count = counts[key]
                    max_route = key
            current_bus.current_route = max_route
            route = Route.query.get_or_404(max_route)
            response = {
            'status': 'success',
                }
            response['route_id'] = route.id
            response['route_name'] = route.name
            return jsonify(response), 201
        response = {
                 'message': 'not found'
                   }
        return jsonify(response), 404 
    elif method == 3:
        print("A model would do the assigning")
    else:
        print("There are no other methods")

@app.route("/api/determine_route",methods = ['GET' , 'POST']) 
# input arguments in request: station_names, bus_id
def DetermineRoute():
    data = request.args
    print(data)
    if data and data['station_names'] and data['bus_id']:
        station_names = data['station_names']
        bus_id = data['bus_id']
        # choose a policy
        return policy(2, station_names,bus_id)
    response = {
                 'message': 'insufficient information'
                   }
    return jsonify(response), 404 

@app.route("/api/bus_arrival",methods = ['GET' , 'POST'])
# input arguments in request: starting_station_name, starting_station_name
def BusArrival():
    def find_difference(location1,location2):
        return random.randint(200,400)
    data =  request.args
    if data['starting_station_name'] and data['starting_station_name']:
        starting_station_name = data['starting_station_name']
        end_station_name = data['end_station_name']
        end_station = Station.query.filter_by(name=end_station_name).first()
        if end_station:
            routes = Route.query.filter_by(ending_station=end_station.id).all()
            buses=[]
            for route in routes:
                buses.extend(Bus.query.filter_by(current_route=route.id).all())
            buses= list(set(buses))
            curr_bus, distance = 1, float('inf')
            starting_station = Station.query.filter_by(station_name=starting_station_name).first()
            for each in buses:
                bus_location = [each.latitude, each.longtiude]
                starting_location = [9.01234, 35.76234]#starting_station.location
                current = find_difference(bus_location, starting_location)
                if current < distance:
                    curr_bus = each.id
                    distance = current
            time = distance / 30
            seats = 100 - curr_bus.count
            response = {
            'status': 'success',
                }
            response['time'] = time
            response['seats'] = seats
            response['distance'] = distance
            return jsonify(response), 201
    response = {
                 'message': 'insufficient information'
                   }
    return jsonify(response), 404 

@app.route("/api/available_seats",methods = ['GET' , 'POST'])
# input arguments in request: bus_id
def AvailableSeats():
    data = request.args
    if data['bus_id']:
        bus_id = data['bus_id']
        current_bus = Bus.query.get(bus_id)
        if current_bus:
            seats = 100 - current_bus.current_count
            response = {
                'status': 'success',
                    }
            response['seats'] = seats
            return jsonify(response), 201
    response = {
                 'message': 'insufficient information'
                   }
    return jsonify(response), 404 

@app.route("/Dashoard")
def Dashboard():
    if current_user.is_authenticated and current_user.role == "Admin":
        redirect("dashboard.html")

@app.route("/login" , methods = ['GET' , 'POST'])
# input arguments in request: username, password
def loginpage():
    data = request.args
    if data['username'] and data['password']:
        username = data['username']
        password = data['password']
        user = User.query.filter_by(uname = username).first()
        if user and user.role == 'driver' and pwd.check_password_hash(user.password , password) :
            #login_user(user)
            bus = Bus.query.filter_by(driver=user.id).first()
            response = {
                'status': 'success',
                    }
            if bus:
                response['bus_id'] = bus.id
            return jsonify(response), 201
        else :
            response = {
                 'message': 'Incorrect Username or Password'
                   }
            return jsonify(response), 404
    
    if current_user.is_authenticated and form.validate():
        flash("You are already logged in." , "warning")
        return redirect(url_for("homepage"))
    form = LoginForm(request.form)
    if request.method == "POST":
        member = User.query.filter_by(uname = form.uname.data).first()
        if member and pwd.check_password_hash(member.password , form.password.data) :
            login_user(member)
            flash("Welcome, %s!" % (form.uname.data) , "success")
            return redirect(url_for("homepage"))
        else:
            flash("Username or Password doesn't match, please try again." , "danger")
            return redirect(url_for("loginpage"))
    return render_template("login.html" , form = form)

@app.route("/logout")
# input arguments in request: username, password
def logoutpage():
    data = request.args
    if data['username'] and data['password']:
        response = {
                 'message': 'success'
                   }
        return jsonify(response), 200
    logout_user()
    flash("Successfuly logged out." , "success")
    return redirect(url_for("homepage"))
