from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from .models import Record


def home(request):
    records = Record.objects.all()

    # Check to see if logging in

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        # Authenticate
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "You have been login successfully")
            return redirect("home")

        else:
            messages.success(request, "There was an error while logging in try again")
            return redirect("home")

    else:
        return render(request, 'home.html', {"records": records})


# def login_user(request):
#     pass


def logout_user(request):
    logout(request)
    messages.success(request, "You have been log OUT successfully")
    return redirect("home")


def register_user(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()

            # Authenticate and then Login
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]

            user = authenticate(username=username, password=password)

            # Login
            login(request, user)
            messages.success(request, 'You have successfully registered ! ! !')
            return redirect("home")

    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form': form})

    return render(request, 'register.html', {'form': form})


def customer_record(request, primary_key):
    if request.user.is_authenticated:
        # Look Up Records
        customer_record = Record.objects.get(id=primary_key)
        return render(request, 'record.html', {'customer_record': customer_record})

    else:
        messages.success(request, "You must be logged in to view that page !!! ")
        return redirect("home")


def delete_record(request, primary_key):
    if request.user.is_authenticated:
        delete_it = Record.objects.get(id=primary_key)
        delete_it.delete()
        messages.success(request, "Record Deleted Successfully .")
        return redirect("home")
    else:
        messages.success(request, "You must be logged in to delete a record !!! ")
        return redirect("home")


def add_record(request):
    if request.user.is_authenticated:

        form = AddRecordForm(request.POST or None)

        if request.method == "POST":
            if form.is_valid():
                add_record = form.save()
                messages.success(request, "Record added Successfully .")
                return redirect("home")

        return render(request, "add_record.html", {"form":form})

    else:
        messages.success(request, "You must be logged in to add a record !!! ")
        return redirect("home")


def update_record(request, primary_key):

    if request.user.is_authenticated:
        current_record = Record.objects.get(id=primary_key)
        form = AddRecordForm(request.POST or None, instance=current_record)

        if form.is_valid():
            form.save()
            messages.success(request, "Record has been updated Successfully .")
            return redirect("home")

        return render(request, "update_record.html", {"form":form})

    else:
        messages.success(request, "You must be logged in to update a record !!! ")
        return redirect("home")
