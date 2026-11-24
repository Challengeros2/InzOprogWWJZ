        // ==========================================
        // APPLICATION STATE: persistent records loaded from Flask API
        // ==========================================

        const GASTRO_MENU = [
            { id: 'm1', name: 'Zapiekanka tradycyjna', price: 18.00, icon: 'fa-bread-slice' },
            { id: 'm2', name: 'Frytki duże z sosami', price: 14.00, icon: 'fa-bowl-rice' },
            { id: 'm3', name: 'Hot Dog amerykański', price: 15.00, icon: 'fa-hotdog' },
            { id: 'm4', name: 'Lody włoskie (dwusmak)', price: 10.00, icon: 'fa-ice-cream' },
            { id: 'm5', name: 'Napój gazowany 0.5L', price: 8.00, icon: 'fa-bottle-water' },
            { id: 'm6', name: 'Kawa Espresso / Cappuccino', price: 12.00, icon: 'fa-mug-hot' }
        ];

        // Records are loaded from SQLite via /api/state.
        let state = {
            wristbands: {},
            orders: [],
            attractions: [],
            schedules: [ // v2 example: not yet saved in SQLite
                { id: 1, employee: "Jan Kowalski (Kasjer)", location: "Kasa Główna", hours: "10:00 - 18:00" },
                { id: 2, employee: "Anna Nowak (Opiekun)", location: "Diabelski Młyn", hours: "10:00 - 18:00" },
                { id: 3, employee: "Piotr Wiśniewski (Technik)", location: "Cały Park", hours: "09:00 - 17:00" },
                { id: 4, employee: "Maria Zielińska (Kucharz)", location: "Strefa Gastro", hours: "10:00 - 19:00" }
            ],
            currentCart: []
        };

        // One helper for every HTTP request. Non-2xx HTTP responses become errors.
        async function api(path, method = 'GET', data = null) {
            const options = { method, headers: { 'Content-Type': 'application/json' } };
            if (data !== null) options.body = JSON.stringify(data);
            let response;
            try {
                response = await fetch(path, options);
            } catch (err) {
                throw new Error('Brak połączenia z lokalnym serwerem Flask.');
            }
            const result = await response.json();
            if (!response.ok) throw new Error(result.error || `Błąd HTTP ${response.status}`);
            return result;
        }

        async function refreshState() {
            const data = await api('/api/state');
            state.wristbands = data.wristbands;
            state.orders = data.orders;
            state.attractions = data.attractions;
            renderGastroMenu();
            renderKitchenOrders();
            renderAttractions();
            renderSchedules();
            setupGateAttractionSelect();
            updatePresetTagButtons();
        }

        // ==========================================
        // INITIALIZATION & TAB SWITCHING
        // ==========================================

        window.onload = async function() {
            try {
                await refreshState();
            } catch (err) {
                showToast(err.message + ' Sprawdź uruchomienie bazy danych.', 'error');
            }
            function updateClock() {
                const clock = document.getElementById('current-time-display');
                if (clock) clock.innerText = new Date().toLocaleTimeString('pl-PL', {
                    hour: '2-digit', minute: '2-digit'
                });
            }
            updateClock();
            setInterval(updateClock, 1000);
        };

        function switchRole(role) {
            // Hide all screens
            const screens = ['kasjer', 'kucharz', 'technik', 'menedzer', 'gost'];
            screens.forEach(s => {
                document.getElementById(`screen-${s}`).classList.add('hidden');
                
                // Desktop nav tabs update
                const tab = document.getElementById(`tab-${s}`);
                if (tab) {
                    tab.classList.remove('tab-active');
                    tab.classList.add('tab-inactive');
                }

                // Mobile nav tabs update
                const mtab = document.getElementById(`mtab-${s}`);
                if (mtab) {
                    mtab.classList.remove('bg-brand-600', 'text-white');
                    mtab.classList.add('text-slate-300');
                }
            });

            // Show selected screen
            document.getElementById(`screen-${role}`).classList.remove('hidden');

            // Activate Tab
            const activeTab = document.getElementById(`tab-${role}`);
            if (activeTab) {
                activeTab.classList.remove('tab-inactive');
                activeTab.classList.add('tab-active');
            }

            const activeMTab = document.getElementById(`mtab-${role}`);
            if (activeMTab) {
                activeMTab.classList.add('bg-brand-600', 'text-white');
                activeMTab.classList.remove('text-slate-300');
            }
        }

        function showToast(message, type = 'info') {
            const container = document.getElementById('toast-container');
            const toast = document.createElement('div');
            const colors = { info: 'bg-slate-800', success: 'bg-emerald-600',
                             error: 'bg-rose-600', warning: 'bg-amber-600' };
            toast.className = `${colors[type] || colors.info} text-white text-xs px-4 py-3 rounded-lg shadow-xl`;
            toast.textContent = message; // Text, not HTML: safe for arbitrary messages
            container.appendChild(toast);
            setTimeout(() => toast.remove(), 4000);
        }

        // ==========================================
        // 1. KASJER LOGIC
        // ==========================================

        function togglePassInputs() {
            const type = document.getElementById('pass-type').value;
            if (type === 'tokens') {
                document.getElementById('token-input-group').classList.remove('hidden');
                document.getElementById('pass-input-group').classList.add('hidden');
            } else {
                document.getElementById('token-input-group').classList.add('hidden');
                document.getElementById('pass-input-group').classList.remove('hidden');
            }
        }

        async function handleWristbandSale(e) {
            e.preventDefault();
            const type = document.getElementById('pass-type').value;
            const reservation = document.getElementById('res-search-id').value.trim();
            const data = { type, owner: reservation ? `Rezerwacja ${reservation}` : 'Gość' };
            if (type === 'tokens') {
                data.tokens = document.getElementById('token-count').value;
            } else {
                data.days = document.getElementById('pass-duration').value;
            }
            try {
                const response = await api('/api/wristbands', 'POST', data);
                await refreshState();
                showToast(`Wydano opaskę ${response.wristband.id}!`, 'success');
                document.getElementById('res-search-id').value = '';
            } catch (err) { showToast(err.message, 'error'); }
        }

        async function handleRecharge() {
            const id = document.getElementById('recharge-tag').value.trim().toUpperCase();
            const amount = document.getElementById('recharge-amount').value;
            if (!id) { showToast('Podaj identyfikator opaski.', 'error'); return; }
            try {
                const data = await api(`/api/wristbands/${encodeURIComponent(id)}/recharge`, 'POST', { amount });
                await refreshState();
                showToast(`Opaska ${id}: ${data.wristband.balance} żetonów.`, 'success');
                document.getElementById('recharge-amount').value = '';
            } catch (err) { showToast(err.message, 'error'); }
        }

        async function checkWristbandBalance() {
            const id = document.getElementById('recharge-tag').value.trim().toUpperCase();
            if (!id) { showToast('Podaj identyfikator opaski.', 'error'); return; }
            try {
                const data = await api(`/api/wristbands/${encodeURIComponent(id)}`);
                const band = data.wristband;
                const info = band.type === 'pass'
                    ? `Karnet ważny do: ${band.valid_until?.replace('T', ' ')}`
                    : `Saldo: ${band.balance} żetonów`;
                showToast(`Opaska ${id}. ${info}`, 'info');
            } catch (err) { showToast(err.message, 'error'); }
        }

        function renderGastroMenu() {
            const container = document.getElementById('gastro-menu-items');
            container.innerHTML = GASTRO_MENU.map(item => `
                <div class="flex items-center justify-between p-2.5 rounded-lg border border-slate-100 hover:border-slate-300 hover:bg-slate-50 transition">
                    <div class="flex items-center gap-3">
                        <div class="w-8 h-8 rounded bg-amber-100 text-amber-700 flex items-center justify-center text-xs">
                            <i class="fa-solid ${item.icon}"></i>
                        </div>
                        <div>
                            <p class="text-sm font-semibold text-slate-800">${item.name}</p>
                            <p class="text-xs text-slate-500">${item.price.toFixed(2)} PLN</p>
                        </div>
                    </div>
                    <button onclick="addToOrder('${item.id}')" class="bg-slate-800 text-white p-2 rounded-md hover:bg-brand-600 text-xs transition">
                        <i class="fa-solid fa-plus"></i>
                    </button>
                </div>
            `).join('');
        }

        function addToOrder(itemId) {
            const menuItem = GASTRO_MENU.find(m => m.id === itemId);
            const existing = state.currentCart.find(c => c.id === itemId);

            if (existing) {
                existing.qty++;
            } else {
                state.currentCart.push({ ...menuItem, qty: 1 });
            }
            renderCurrentTicket();
        }

        function updateCartQty(itemId, change) {
            const item = state.currentCart.find(c => c.id === itemId);
            if (item) {
                item.qty += change;
                if (item.qty <= 0) {
                    state.currentCart = state.currentCart.filter(c => c.id !== itemId);
                }
            }
            renderCurrentTicket();
        }

        function renderCurrentTicket() {
            const list = document.getElementById('order-ticket-list');
            const submitBtn = document.getElementById('btn-submit-order');
            const totalEl = document.getElementById('order-total-price');

            if (state.currentCart.length === 0) {
                list.innerHTML = `<p class="text-slate-400 text-xs italic text-center py-6">Brak pozycji w zamówieniu</p>`;
                submitBtn.disabled = true;
                totalEl.innerText = '0.00 PLN';
                return;
            }

            submitBtn.disabled = false;
            let total = 0;

            list.innerHTML = state.currentCart.map(item => {
                const subtotal = item.price * item.qty;
                total += subtotal;
                return `
                    <div class="flex items-center justify-between border-b border-slate-200 pb-1.5">
                        <div class="flex-grow pr-2">
                            <p class="text-xs font-medium text-slate-800">${item.name}</p>
                            <p class="text-[10px] text-slate-500">${item.price.toFixed(2)} PLN/szt.</p>
                        </div>
                        <div class="flex items-center gap-1.5">
                            <button onclick="updateCartQty('${item.id}', -1)" class="w-5 h-5 bg-slate-200 rounded flex items-center justify-center text-xs text-slate-700 font-bold">-</button>
                            <span class="text-xs font-bold w-4 text-center">${item.qty}</span>
                            <button onclick="updateCartQty('${item.id}', 1)" class="w-5 h-5 bg-slate-200 rounded flex items-center justify-center text-xs text-slate-700 font-bold">+</button>
                        </div>
                    </div>
                `;
            }).join('');

            totalEl.innerText = `${total.toFixed(2)} PLN`;
        }

        async function submitGastroOrder() {
            if (state.currentCart.length === 0) return;
            try {
                const data = await api('/api/orders', 'POST', {
                    items: state.currentCart.map(item => ({ id: item.id, qty: item.qty }))
                });
                state.currentCart = [];
                renderCurrentTicket();
                await refreshState();
                showToast(`Zapisano zamówienie #${data.order.id}`, 'success');
            } catch (err) { showToast(err.message, 'error'); }
        }

        // ==========================================
        // 2. KUCHARZ LOGIC
        // ==========================================

        function renderKitchenOrders() {
            const grid = document.getElementById('kitchen-orders-grid');
            if (state.orders.length === 0) {
                grid.innerHTML = `<div class="col-span-full text-center py-12 text-slate-400">Brak aktywnych zamówień kuchennych</div>`;
                return;
            }

            grid.innerHTML = state.orders.map(order => {
                let statusBadge = '';
                if (order.status === 'Oczekujące') statusBadge = '<span class="bg-amber-100 text-amber-800 text-xs px-2 py-0.5 rounded font-bold">Oczekuje</span>';
                if (order.status === 'W trakcie') statusBadge = '<span class="bg-blue-100 text-blue-800 text-xs px-2 py-0.5 rounded font-bold">W trakcie</span>';
                if (order.status === 'Zrealizowane') statusBadge = '<span class="bg-emerald-100 text-emerald-800 text-xs px-2 py-0.5 rounded font-bold">Gotowe</span>';
                if (order.status === 'Nieodebrane') statusBadge = '<span class="bg-rose-100 text-rose-800 text-xs px-2 py-0.5 rounded font-bold">Nieodebrane</span>';

                return `
                    <div class="bg-white p-4 rounded-xl shadow-sm border border-slate-200 flex flex-col justify-between space-y-3">
                        <div>
                            <div class="flex justify-between items-center border-b pb-2 mb-2">
                                <span class="font-bold text-slate-800">Zamówienie #${order.id}</span>
                                <div class="flex items-center gap-2">
                                    <span class="text-xs text-slate-400">${order.time}</span>
                                    ${statusBadge}
                                </div>
                            </div>
                            <ul class="text-sm space-y-1 my-3">
                                ${order.items.map(i => `<li class="flex justify-between"><span class="text-slate-700">${i.name}</span> <span class="font-bold text-slate-900">x${i.qty}</span></li>`).join('')}
                            </ul>
                        </div>

                        <div class="pt-2 border-t flex gap-1.5">
                            <button onclick="updateOrderStatus(${order.id}, 'W trakcie')" class="flex-1 bg-blue-50 text-blue-700 hover:bg-blue-100 text-xs py-2 rounded font-medium">
                                W trakcie
                            </button>
                            <button onclick="updateOrderStatus(${order.id}, 'Zrealizowane')" class="flex-1 bg-emerald-600 hover:bg-emerald-700 text-white text-xs py-2 rounded font-medium">
                                Gotowe
                            </button>
                            <button onclick="updateOrderStatus(${order.id}, 'Nieodebrane')" class="bg-slate-100 text-slate-600 hover:bg-slate-200 text-xs px-2 rounded font-medium" title="Nieodebrane">
                                <i class="fa-solid fa-xmark"></i>
                            </button>
                        </div>
                    </div>
                `;
            }).join('');
        }

        async function updateOrderStatus(orderId, newStatus) {
            try {
                await api(`/api/orders/${orderId}/status`, 'PATCH', { status: newStatus });
                await refreshState();
                showToast(`Zamówienie #${orderId}: ${newStatus}`, 'info');
            } catch (err) { showToast(err.message, 'error'); }
        }

        // ==========================================
        // 3. TECHNIK LOGIC
        // ==========================================

        function renderAttractions() {
            const grid = document.getElementById('attractions-grid');
            const badgeColors = {
                'Działająca': 'bg-emerald-100 text-emerald-800 border-emerald-300',
                'Uszkodzona': 'bg-rose-100 text-rose-800 border-rose-300',
                'W trakcie naprawy': 'bg-amber-100 text-amber-800 border-amber-300',
                'Zamknięta': 'bg-slate-100 text-slate-700 border-slate-300'
            };
            grid.innerHTML = state.attractions.map(a => `
                <div class="bg-white p-4 rounded-xl shadow-sm border border-slate-200 flex flex-col justify-between gap-3">
                    <div>
                        <div class="flex justify-between items-start gap-2 mb-2">
                            <h4 class="font-bold text-slate-800 text-base">${a.id}. ${a.name}</h4>
                            <span class="text-xs font-semibold px-2 py-0.5 rounded border ${badgeColors[a.status]}">${a.status}</span>
                        </div>
                        <p class="text-xs text-slate-500">Koszt wejścia: ${a.cost} żetonów</p>
                    </div>
                    <div class="pt-3 border-t border-slate-100">
                        <label class="block text-xs text-slate-500 mb-2">Zmień status:</label>
                        <div class="grid grid-cols-2 gap-1.5">
                            <button onclick="changeAttractionStatus(${a.id}, 'Działająca')" class="bg-emerald-100 text-emerald-900 text-xs p-2 rounded">Działająca</button>
                            <button onclick="changeAttractionStatus(${a.id}, 'Uszkodzona')" class="bg-rose-100 text-rose-900 text-xs p-2 rounded">Uszkodzona</button>
                            <button onclick="changeAttractionStatus(${a.id}, 'W trakcie naprawy')" class="bg-amber-100 text-amber-900 text-xs p-2 rounded">W naprawie</button>
                            <button onclick="changeAttractionStatus(${a.id}, 'Zamknięta')" class="bg-slate-100 text-slate-900 text-xs p-2 rounded">Zamknięta</button>
                        </div>
                    </div>
                </div>`).join('');
        }

        async function changeAttractionStatus(attrId, newStatus) {
            try {
                const data = await api(`/api/attractions/${attrId}/status`, 'PATCH', { status: newStatus });
                await refreshState();
                showToast(`Atrakcja '${data.attraction.name}': ${newStatus}`, 'success');
            } catch (err) { showToast(err.message, 'error'); }
        }

        // ==========================================
        // 4. MENEDŻER LOGIC
        // ==========================================

        function renderSchedules() {
            const tbody = document.getElementById('schedule-table-body');
            tbody.innerHTML = state.schedules.map(sch => `
                <tr class="hover:bg-slate-50">
                    <td class="py-3 px-4 font-semibold text-slate-800">${sch.employee}</td>
                    <td class="py-3 px-4 text-slate-600">${sch.location}</td>
                    <td class="py-3 px-4 text-slate-600">${sch.hours}</td>
                    <td class="py-3 px-4 text-right">
                        <button onclick="deleteSchedule(${sch.id})" class="text-rose-600 hover:text-rose-800 text-xs font-medium">
                            <i class="fa-solid fa-trash mr-1"></i> Usuń
                        </button>
                    </td>
                </tr>
            `).join('');
        }

        function handleAssignSchedule(e) {
            e.preventDefault();
            const emp = document.getElementById('sch-employee').value;
            const loc = document.getElementById('sch-attraction').value;
            const from = document.getElementById('sch-time-from').value;
            const to = document.getElementById('sch-time-to').value;

            // Conflict Check
            const conflict = state.schedules.find(s => s.employee === emp);
            if (conflict) {
                if (!confirm(`Ostrzeżenie: Pracownik ${emp} ma już przypisanie (${conflict.location}). Czy chcesz mimo to dopisać nowe stanowisko?`)) {
                    return;
                }
            }

            state.schedules.push({
                id: state.schedules.length + 1,
                employee: emp,
                location: loc,
                hours: `${from} - ${to}`
            });

            renderSchedules();
            showToast(`Dodano nowy grafik dla ${emp}!`, 'success');
        }

        function deleteSchedule(id) {
            state.schedules = state.schedules.filter(s => s.id !== id);
            renderSchedules();
            showToast('Wpis usunięty z harmonogramu', 'info');
        }

        // ==========================================
        // 5. GOŚĆ / BRAMKA LOGIC
        // ==========================================

        function setupGateAttractionSelect() {
            const select = document.getElementById('gate-attraction-select');
            const previous = select.value;
            select.innerHTML = state.attractions.map(a => `
                <option value="${a.id}">${a.name} (${a.cost} żetonów) - [${a.status}]</option>
            `).join('');
            if (state.attractions.some(a => String(a.id) === previous)) select.value = previous;
        }

        function updatePresetTagButtons() {
            const container = document.getElementById('preset-tags');
            container.innerHTML = Object.keys(state.wristbands).map(tag => `
                <button onclick="document.getElementById('gate-tag-input').value='${tag}'" class="bg-slate-100 hover:bg-slate-200 text-slate-700 text-[11px] px-2 py-1 rounded font-mono border">
                    ${tag} (${state.wristbands[tag].type === 'pass' ? 'Karnet' : state.wristbands[tag].balance + 'ż'})
                </button>
            `).join('');
        }

        async function scanWristband() {
            const id = document.getElementById('gate-tag-input').value.trim().toUpperCase();
            const attrId = document.getElementById('gate-attraction-select').value;
            const card = document.getElementById('gate-status-card');
            const icon = document.getElementById('gate-icon-container');
            const status = document.getElementById('gate-status-text');
            const detail = document.getElementById('gate-subtext');
            const info = document.getElementById('gate-account-info');
            if (!id) { showToast('Podaj ID opaski.', 'error'); return; }
            try {
                const data = await api('/api/entry', 'POST', { wristband_id: id, attraction_id: attrId });
                card.className = 'text-white p-6 rounded-xl flex flex-col items-center justify-center text-center space-y-4 bg-slate-900';
                info.classList.add('hidden');
                info.textContent = '';
                if (data.allowed) {
                    card.classList.add('bg-emerald-900');
                    icon.innerHTML = '<i class="fa-solid fa-door-open"></i>';
                    status.textContent = 'BRAMKA OTWARTA';
                    detail.textContent = data.type === 'pass'
                        ? 'Karnet ważny. Zezwolono na wejście.'
                        : `Pobrano ${data.deducted} żetonów. Zezwolono na wejście.`;
                    info.classList.remove('hidden');
                    info.textContent = data.type === 'pass'
                        ? `Opaska ${data.wristband_id} • ${data.attraction} • Karnet czasowy`
                        : `Opaska ${data.wristband_id} • Pozostało: ${data.remaining} żetonów`;
                } else {
                    card.classList.add('bg-rose-950');
                    icon.innerHTML = '<i class="fa-solid fa-ban"></i>';
                    status.textContent = 'ODMOWA WEJŚCIA';
                    detail.textContent = data.message;
                }
                await refreshState();
            } catch (err) { showToast(err.message, 'error'); }
        }
    
