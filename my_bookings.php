<?php $pageTitle = 'My bookings'; include 'includes/header.php'; require_login();
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    check_csrf();
    db()->prepare("UPDATE bookings SET status='Cancelled' WHERE id=? AND user_id=? AND status<>'Cancelled'")
        ->execute([(int)$_POST['cancel'], $_SESSION['uid']]);
    header('Location: my_bookings.php'); exit;
}
$st = db()->prepare('SELECT b.*, p.title, p.destination FROM bookings b JOIN packages p ON p.id=b.package_id WHERE b.user_id=? ORDER BY b.created_at DESC');
$st->execute([$_SESSION['uid']]); $rows = $st->fetchAll(); ?>
<section class="wrap">
  <h1>My bookings</h1>
  <?php if (isset($_GET['booked'])): ?><p class="ok">Booking received. We'll confirm it shortly.</p><?php endif; ?>
  <?php if (!$rows): ?><p class="empty">You have no bookings yet. <a href="packages.php">Find a trip</a></p>
  <?php else: ?>
  <div class="scroll"><table>
    <tr><th>Trip</th><th>Travel date</th><th>Travellers</th><th>Total</th><th>Status</th><th></th></tr>
    <?php foreach ($rows as $b): ?>
    <tr>
      <td><?= e($b['title']) ?><br><small><?= e($b['destination']) ?></small></td>
      <td><?= e($b['travel_date']) ?></td><td><?= (int)$b['travellers'] ?></td><td><?= inr($b['total']) ?></td>
      <td><span class="tag <?= strtolower($b['status']) ?>"><?= e($b['status']) ?></span></td>
      <td><?php if ($b['status'] !== 'Cancelled'): ?>
        <form method="post" data-confirm="Cancel this booking?"><input type="hidden" name="csrf" value="<?= csrf() ?>">
        <button class="btn small ghost" name="cancel" value="<?= (int)$b['id'] ?>">Cancel</button></form><?php endif; ?></td>
    </tr><?php endforeach; ?>
  </table></div><?php endif; ?>
</section>
<?php include 'includes/footer.php'; ?>
