<link rel="stylesheet" href="./style.css">

<nav class="navbar navbar-expand-lg navbar-light bg-light">
  <div class="container-fluid">
    <a class="navbar-brand" href="#">YOGI</a>
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarSupportedContent">
      <ul class="navbar-nav me-auto mb-2 mb-lg-0">
        <li class="nav-item">
        <a class="nav-link active" href="./landing.php">Home</a>
        </li>
        <li class="nav-item">
        <a class="nav-link active" href="./signup.php">SignUp</a>
        </li>
        <li class="nav-item">
        <a class="nav-link active" aria-current="page" href="./login.php">Login</a>
        </li>
          <ul class="dropdown-menu" aria-labelledby="navbarDropdown">
            <li><a class="nav-link" href="./signup.php">SignUp</a></li>
            <li><a class="nav-link active" aria-current="page" href="./login.php">Login</a></li>
            <li><hr class="dropdown-divider"></li>
            <li><a class="dropdown-item" href="#">Something else here</a></li>
          </ul>
      </ul>
      <form class="d-flex">
        <input class="form-control me-2" type="search" placeholder="Search" aria-label="Search">
        <button class="btn btn-outline-success" type="submit">Search</button>
      </form>
    </div>
  </div>
</nav>