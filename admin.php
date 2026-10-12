<?php $pageTitle = 'Admin'; include 'includes/header.php'; require_admin();
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    check_csrf();
    if (isset($_POST['add'])) {
        db()->prepare('INSERT INTO packages (title,destination,country,region,category,days,price,summary,details,keywords) VALUES (?,?,?,?,?,?,?,?,?,?)')
          ->execute([$_POST['title'],$_POST['destination'],$_POST['country'],$_POST['region'],$_POST['category'],(int)$_POST['days'],(float)$_POST['price'],$_POST['summary'],$_POST['details'],$_POST['keywords']]);
    } elseif (isset($_POST['delete'])) {
        db()->prepare('DELETE FROM packages WHERE id=?')->execute([(int)$_POST['delete']]);
    } elseif (isset($_POST['status'])) {
        $s = in_array($_POST['status'], ['Pending','Confirmed','Cancelled']) ? $_POST['status'] : 'Pending';
        db()->prepare('UPDATE bookings SET status=? WHERE id=?')->execute([$s, (int)$_POST['booking']]);
    }
    header('Location: admin.php'); exit;
}
$packs = db()->query('SELECT * FROM packages ORDER BY id DESC')->fetchAll();
$books = db()->query('SELECT b.*, u.name uname, p.title FROM bookings b JOIN users u ON u.id=b.user_id JOIN packages p ON p.id=b.package_id ORDER BY b.created_at DESC')->fetchAll(); ?>
<section class="wrap">
  <h1>Admin dashboard</h1>
  <h2>Bookings</h2>
  <div class="scroll"><table>
    <tr><th>Customer</th><th>Trip</th><th>Date</th><th>Total</th><th>Status</th></tr>
    <?php foreach ($books as $b): ?><tr>
      <td><?= e($b['uname']) ?></td><td><?= e($b['title']) ?></td><td><?= e($b['travel_date']) ?></td><td><?= inr($b['total']) ?></td>
      <td><form method="post" class="inline"><input type="hidden" name="csrf" value="<?= csrf() ?>"><input type="hidden" name="booking" value="<?= (int)$b['id'] ?>">
        <select name="status" onchange="this.form.submit()"><?php foreach (['Pending','Confirmed','Cancelled'] as $s): ?><option <?= $b['status']===$s?'selected':'' ?>><?= $s ?></option><?php endforeach; ?></select></form></td>
    </tr><?php endforeach; ?>
  </table></div>
  <h2>Packages</h2>
  <div class="scroll"><table>
    <?php foreach ($packs as $p): ?><tr><td><?= e($p['title']) ?></td><td><?= inr($p['price']) ?></td>
      <td><form method="post" data-confirm="Delete this package and its bookings?"><input type="hidden" name="csrf" value="<?= csrf() ?>"><button class="btn small ghost" name="delete" value="<?= (int)$p['id'] ?>">Delete</button></form></td></tr><?php endforeach; ?>
  </table></div>
  <h2>Add a package</h2>
  <form method="post" class="stack">
    <input type="hidden" name="csrf" value="<?= csrf() ?>">
    <label>Title <input name="title" required></label>
    <label>Destination <input name="destination" required></label>
    <label>Country <input name="country" value="India" required></label>
    <label>Region <select name="region"><?php foreach (REGIONS as $r): ?><option><?= $r ?></option><?php endforeach; ?></select></label>
    <label>Image keywords (comma separated, e.g. goa,beach) <input name="keywords" required></label>
    <label>Category <select name="category"><?php foreach (CATEGORIES as $c): ?><option><?= $c ?></option><?php endforeach; ?></select></label>
    <label>Days <input type="number" name="days" min="1" required></label>
    <label>Price per person (₹) <input type="number" name="price" min="1" step="0.01" required></label>
    <label>Summary <input name="summary" maxlength="255" required></label>
    <label>Itinerary and inclusions <textarea name="details" rows="4" required></textarea></label>
    <button class="btn" name="add" value="1">Add package</button>
  </form>
</section>
<?php include 'includes/footer.php'; ?>
