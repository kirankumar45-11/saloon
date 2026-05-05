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

    // ── Show available slots for selected expert + date ──
    const expertSelect = document.getElementById('id_expert');
    const dateInput    = document.getElementById('id_date');
    const slotsContainer = document.getElementById('slots_container');
    const timeInput    = document.getElementById('id_time');
    const timeDisplay  = document.getElementById('selected_time_display');

    function loadAvailability() {
        if (!slotsContainer || !dateInput) return;
        
        const expertId = expertSelect ? expertSelect.value : null;
        const dateVal  = dateInput.value;
        
        if (!dateVal) { 
            slotsContainer.innerHTML = '<p class="text-muted small italic">Please select a date to see available slots.</p>';
            return; 
        }

        slotsContainer.innerHTML = '<div class="text-muted small"><i class="fa-solid fa-spinner fa-spin me-1"></i>Fetching slots...</div>';

        // Choose API based on whether an expert is selected
        let url = expertId 
            ? '/api/availability/' + expertId + '/?date=' + dateVal
            : '/api/availability/all/?date=' + dateVal;

        fetch(url)
            .then(r => r.json())
            .then(slots => {
                slotsContainer.innerHTML = '';
                if (slots.length === 0) {
                    slotsContainer.innerHTML = '<p class="text-danger small">No slots available for this date.</p>';
                } else {
                    slots.forEach(slot => {
                        const btn = document.createElement('div');
                        btn.className = 'slot-item' + (slot.available ? '' : ' booked');
                        
                        // Time label
                        const timeLabel = document.createElement('span');
                        timeLabel.textContent = slot.time;
                        btn.appendChild(timeLabel);

                        // Seat count label (if available)
                        if (slot.available_seats !== undefined) {
                            const seatLabel = document.createElement('span');
                            seatLabel.className = 'seat-count';
                            seatLabel.textContent = slot.available_seats + ' seats free';
                            btn.appendChild(seatLabel);
                        }
                        
                        if (slot.available) {
                            btn.addEventListener('click', function() {
                                // Clear previous selection
                                document.querySelectorAll('.slot-item').forEach(s => s.classList.remove('selected'));
                                // Set current selection
                                btn.classList.add('selected');
                                timeInput.value = slot.time;
                                if (timeDisplay) timeDisplay.textContent = 'Selected: ' + slot.time;
                                
                                // If no expert was selected, maybe prompt or auto-assign?
                                // For now, we'll let the user pick an expert if they haven't.
                                if (!expertId) {
                                    // Optionally highlight that an expert still needs to be picked
                                    if (expertSelect) {
                                        expertSelect.classList.add('is-invalid');
                                        setTimeout(() => expertSelect.classList.remove('is-invalid'), 2000);
                                    }
                                }
                            });
                        } else {
                            btn.title = 'Fully booked';
                        }
                        slotsContainer.appendChild(btn);
                    });
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
