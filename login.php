<?php
$alert=false;
if ($_SERVER["REQUEST_METHOD"]=="POST"){

    include 'partials/_dbconnect.php';
    $username=$_POST["username"];
    $email=$_POST["Email"];
    $password=$_POST["password"];   
    $sql="Select * from users where username='$username' AND email='$email' AND password='$password' ";
    $result=mysqli_query($conn,$sql);
    $num=mysqli_num_rows($result);
    if ($num==1){
      $login=true;
      session_start();
      $_SESSION["loggedin"]=true;
      $_SESSION["username"]=$username;
      header("location: signup.php");
    }
    // else{
    //   $showerror
    // }
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

    <title>LogIn!</title>
  </head>
<body>
<?php require 'partials/_nav.php' ?>
<div class="container">
    <form action="/YOGI/login.php" method="post">
            <h1>LogIn Form!</h1>
          <div class="form-row">
                <div class="col-md-4 mb-3">
                <label for="username">Username</label>
                <input type="text" class="form-control is-valid" id="username" placeholder="Enter your username" name="username" required>
                <div class="valid-feedback">
                </div>
                </div>
            </div>
            <div class="form-row">
                <div class="col-md-4 mb-3">
                <label for="Email">Email Id</label>
                <input type="email" class="form-control" id="Email" name="Email" aria-describedby="emailHelp" placeholder="Enter email" required>
              </div>
            </div> 
            <div class="form-row">
              <div class="col-md-4 mb-3">
                <label for="password">Password</label>
                <input type="password" class="form-control" id="password" placeholder="Password" name="password" required>
              </div>
            </div>
            <button type="submit" class="btn btn-primary">Login</button>
        </form>
    </div>
    <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/popper.js@1.14.7/dist/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@4.3.1/dist/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>
</body>
</html>