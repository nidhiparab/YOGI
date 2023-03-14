<?php
$alert=false;
if ($_SERVER["REQUEST_METHOD"]=="POST"){

    include 'partials/_dbconnect.php';
    $Fname=$_POST["Fname"];
    $Lname=$_POST["Lname"];
    $email=$_POST["Email"];
    $height=$_POST["height"];
    $weight=$_POST["weight"];
    $gender=$_POST["gender"];
    $password=$_POST["password"];
    $cpassword=$_POST["cpassword"];
    $exists=false;
    if(($password==$cpassword) && $exists==false){
        $sql="INSERT INTO `users` (`Fname`, `Lname`, `email`, `height`, `weight`,`gender`, `password`) VALUES ( '$Fname', '$Lname', '$email', '$height', '$weight', '$gender', '$password')";
        $result=mysqli_query($conn,$sql);
        if ($result){
            $alert=true;
        }
    }
}
?>


<!DOCTYPE html>
<html lang="en">
<head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    
    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.3.1/dist/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">

    <title>Sign Up!</title>
  </head>
<body>
<?php require 'partials/_nav.php' ?>
<div class="container">
    <form action="/LOC 5.0/signup.php" method="post">
            <h1>Sign Up Form!</h1>
        <div class="form-row">
                <div class="col-md-4 mb-3">
                <label for="Fname">First name</label>
                <input type="text" class="form-control is-valid" id="Fname" placeholder="First name" name="Fname" required>
                <div class="valid-feedback">
                </div>
                </div>
                <div class="col-md-4 mb-3">
                <label for="Lname">Last name</label>
                <input type="text" class="form-control is-valid" id="Lname"  name="Lname" placeholder="Last name" required>
                <div class="valid-feedback">
                </div>
                </div>
            </div>
            <div class="form-group">
                <label for="Email">Email address</label>
                <input type="email" class="form-control" id="Email" name="Email" aria-describedby="emailHelp" placeholder="Enter email" required>
            </div>
            <div class="form-group">
                <label for="height">Height (in cm)</label>
                <input type="text" class="form-control" id="height" name="height" placeholder="Enter your height" required>
            </div>
            <div class="form-group">
                <label for="weight">Weight (in kg)</label>
                <input type="text" class="form-control" id="weight" name="weight" placeholder="Enter your weight" required>
            </div>
            <p>Gender</p>
            <div class="form-check">
                <input class="form-check-input" type="radio" name="gender" id="male">
                <label class="form-check-label" for="male">
                    Male
                </label>
            </div>
            <div class="form-check">
                <input class="form-check-input" type="radio" name="gender" id="female" checked>
                <label class="form-check-label" for="female">
                    Female
                </label>
            </div>
            <br>
            <div class="form-group">
                <label for="password">Password</label>
                <input type="password" class="form-control" id="password" placeholder="Password" name="password" required>
            </div>
            <div class="form-group">
                <label for="cpassword">Confirm Password</label>
                <input type="password" class="form-control" id="cpassword" name ="cpassword" placeholder="Password" required>
            </div>
            <button type="submit" class="btn btn-primary">SignUp</button>
        </form>
    </div>
    <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/popper.js@1.14.7/dist/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@4.3.1/dist/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>
</body>
</html>