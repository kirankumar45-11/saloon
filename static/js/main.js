/* ====================================
   GLAMOUR SALON — Main JavaScript
   ==================================== */
document.addEventListener('DOMContentLoaded', function () {

    // ── Restrict date inputs to today or later ──
    document.querySelectorAll('input[type="date"]').forEach(function (el) {
        el.setAttribute('min', new Date().toISOString().split('T')[0]);
    });

    // ── Dynamic service loading by category ──
    const catSelect   = document.getElementById('category_select');
    const svcSelect   = document.getElementById('id_service');

    if (catSelect && svcSelect) {
        catSelect.addEventListener('change', function () {
            const catId = this.value;
            svcSelect.innerHTML = '<option value="">Loading...</option>';
            svcSelect.disabled = true;

            if (!catId) {
                svcSelect.innerHTML = '<option value="">Select a service...</option>';
                return;
            }

            fetch('/api/services/' + catId + '/')
                .then(r => r.json())
                .then(data => {
                    svcSelect.innerHTML = '<option value="">Select a service...</option>';
                    data.forEach(s => {
                        const opt = document.createElement('option');
                        opt.value = s.id;
                        opt.textContent = s.name + ' — $' + s.price + ' (' + s.duration_minutes + ' min)';
                        svcSelect.appendChild(opt);
                    });
                    svcSelect.disabled = false;
                });
        });
    }

    // ── Show booked times for selected expert + date ──
    const expertSelect = document.getElementById('id_expert');
    const dateInput    = document.getElementById('id_date');
    const bookedInfo   = document.getElementById('booked_times');

    function loadAvailability() {
        if (!expertSelect || !dateInput || !bookedInfo) return;
        const expertId = expertSelect.value;
        const dateVal  = dateInput.value;
        if (!expertId || !dateVal) { bookedInfo.innerHTML = ''; return; }

        fetch('/api/availability/' + expertId + '/?date=' + dateVal)
            .then(r => r.json())
            .then(times => {
                if (times.length === 0) {
                    bookedInfo.innerHTML = '<span class="text-success"><i class="fa-solid fa-circle-check me-1"></i>All times available</span>';
                } else {
                    bookedInfo.innerHTML = '<span class="text-danger"><i class="fa-solid fa-clock me-1"></i>Already booked: ' + times.join(', ') + '</span>';
                }
            });
    }

    if (expertSelect) expertSelect.addEventListener('change', loadAvailability);
    if (dateInput) dateInput.addEventListener('change', loadAvailability);

    // ── Payment option selection ──
    document.querySelectorAll('.payment-option').forEach(function (el) {
        el.addEventListener('click', function () {
            document.querySelectorAll('.payment-option').forEach(o => o.classList.remove('selected'));
            this.classList.add('selected');
            const radio = this.querySelector('input[type="radio"]');
            if (radio) radio.checked = true;
        });
    });

    // ── Auto-dismiss Bootstrap alerts after 5s ──
    document.querySelectorAll('.alert-dismissible').forEach(function (el) {
        setTimeout(function () {
            var bsAlert = bootstrap.Alert.getOrCreateInstance(el);
            bsAlert.close();
        }, 5000);
    });

    // ── Print invoice ──
    const printBtn = document.getElementById('print_invoice');
    if (printBtn) {
        printBtn.addEventListener('click', function () {
            window.print();
        });
    }
});
