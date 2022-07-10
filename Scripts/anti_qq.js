<script>
let newurl = document.evaluate('//*[@id="url"]/text()', document).iterateNext();
window.location.replace(newurl.textContent)
  </script>
