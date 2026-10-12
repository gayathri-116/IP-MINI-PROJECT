<?php $pageTitle = 'Sign up'; include 'includes/header.php';
$errors = [];
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    check_csrf();
    $name = trim($_POST['name'] ?? ''); $email = strtolower(trim($_POST['email'] ?? '')); $pw = $_POST['password'] ?? '';
    if ($name === '') $errors[] = 'Enter your name.';
    if (!filter_var($email, FILTER_VALIDATE_EMAIL)) $errors[] = 'Enter a valid email address.';
    if (strlen($pw) < 6) $errors[] = 'Password needs at least 6 characters.';
    if (!$errors) {
        $c = db()->prepare('SELECT id FROM users WHERE email=?'); $c->execute([$email]);
        if ($c->fetch()) $errors[] = 'That email is already registered. Try logging in.';
        else {
            db()->prepare('INSERT INTO users (name,email,password) VALUES (?,?,?)')->execute([$name, $email, password_hash($pw, PASSWORD_DEFAULT)]);
            $_SESSION['uid'] = db()->lastInsertId(); $_SESSION['name'] = $name; $_SESSION['role'] = 'user';
            header('Location: packages.php'); exit;
        }
    }
} ?>
<section class="wrap narrow">
  <h1>Create your account</h1>
  <?php foreach ($errors as $er): ?><p class="error"><?= e($er) ?></p><?php endforeach; ?>
  <form method="post" class="stack">
    <input type="hidden" name="csrf" value="<?= csrf() ?>">
    <label>Full name <input name="name" required value="<?= e($_POST['name'] ?? '') ?>"></label>
    <label>Email <input type="email" name="email" required value="<?= e($_POST['email'] ?? '') ?>"></label>
    <label>Password <input type="password" name="password" minlength="6" required></label>
    <button class="btn">Sign up</button>
  </form>
  <p>Already registered? <a href="login.php">Log in</a></p>
</section>
<?php include 'includes/footer.php'; ?>
