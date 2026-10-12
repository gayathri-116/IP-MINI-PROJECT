<?php require_once __DIR__ . '/../config.php'; ?>
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title><?= e($pageTitle ?? 'Wanderly') ?> | Wanderly Tours</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,400;12..96,600;12..96,800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/style.css">
<script src="assets/js/main.js" defer></script>
</head>
<body>
<header class="site">
  <a class="logo" href="index.php">Wanderly</a>
  <button class="burger" aria-label="Menu" aria-expanded="false">Menu</button>
  <nav id="nav">
    <a href="index.php">Home</a>
    <a href="packages.php">Packages</a>
    <a href="about.php">About</a>
    <a href="contact.php">Contact</a>
    <?php if (logged_in()): ?>
      <a href="my_bookings.php">My bookings</a>
      <?php if ($_SESSION['role'] === 'admin'): ?><a href="admin.php">Admin</a><?php endif; ?>
      <a href="logout.php" class="btn small ghost">Log out (<?= e($_SESSION['name']) ?>)</a>
    <?php else: ?>
      <a href="login.php">Log in</a>
      <a href="register.php" class="btn small">Sign up</a>
    <?php endif; ?>
  </nav>
</header>
<main>
