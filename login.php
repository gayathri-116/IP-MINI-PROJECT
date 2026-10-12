<?php $pageTitle = 'Log in'; include 'includes/header.php';
$error = '';
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    check_csrf();
    $st = db()->prepare('SELECT * FROM users WHERE email=?'); $st->execute([strtolower(trim($_POST['email'] ?? ''))]); $u = $st->fetch();
    if ($u && password_verify($_POST['password'] ?? '', $u['password'])) {
        session_regenerate_id(true);
        $_SESSION['uid'] = $u['id']; $_SESSION['name'] = $u['name']; $_SESSION['role'] = $u['role'];
        $next = $_GET['next'] ?? 'packages.php';
        if (!preg_match('/^[\w\-\/\.\?=&%]+$/', $next) || str_contains($next, '//')) $next = 'packages.php';
        header('Location: ' . ltrim($next, '/')); exit;
    }
    $error = 'Email or password is incorrect.';
} ?>
<section class="wrap narrow">
  <h1>Log in</h1>
  <?php if ($error): ?><p class="error"><?= e($error) ?></p><?php endif; ?>
  <form method="post" class="stack">
    <input type="hidden" name="csrf" value="<?= csrf() ?>">
    <label>Email <input type="email" name="email" required></label>
    <label>Password <input type="password" name="password" required></label>
    <button class="btn">Log in</button>
  </form>
  <p>New here? <a href="register.php">Create an account</a></p>
</section>
<?php include 'includes/footer.php'; ?>
