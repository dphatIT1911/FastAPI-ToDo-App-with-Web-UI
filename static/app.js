// API Configuration
const API_BASE_URL = 'http://localhost:8000/api/v1';

// State
let todos = [];
let currentFilter = 'all';
let currentSearch = '';
let currentSort = '-created_at';
let token = localStorage.getItem('todo_token');

// DOM Elements
const authSection = document.getElementById('authSection');
const mainContent = document.getElementById('mainContent');
const userSection = document.getElementById('userSection');
const userEmailSpan = document.getElementById('userEmail');
const logoutBtn = document.getElementById('logoutBtn');

const tabLogin = document.getElementById('tabLogin');
const tabRegister = document.getElementById('tabRegister');
const loginForm = document.getElementById('loginForm');
const registerForm = document.getElementById('registerForm');

const todoInput = document.getElementById('todoInput');
const addTodoForm = document.getElementById('addTodoForm');
const todoList = document.getElementById('todoList');
const searchInput = document.getElementById('searchInput');
const statusFilter = document.getElementById('statusFilter');
const sortOrder = document.getElementById('sortOrder');
const refreshBtn = document.getElementById('refreshBtn');
const loadingSpinner = document.getElementById('loadingSpinner');
const emptyState = document.getElementById('emptyState');
const totalCount = document.getElementById('totalCount');
const completedCount = document.getElementById('completedCount');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    updateAuthState();
    setupEventListeners();
});

// Auth State Management
function updateAuthState() {
    if (token) {
        authSection.style.display = 'none';
        mainContent.style.display = 'block';
        userSection.style.display = 'flex';
        fetchUserInfo();
        loadTodos(true); // pass true to suppress initial toast
    } else {
        authSection.style.display = 'block';
        mainContent.style.display = 'none';
        userSection.style.display = 'none';
    }
}

async function fetchUserInfo() {
    try {
        const response = await fetch(`${API_BASE_URL}/auth/me`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        if (response.ok) {
            const user = await response.json();
            userEmailSpan.textContent = user.email;
        } else {
            handleLogout();
        }
    } catch (error) {
        console.error('Error fetching user info:', error);
    }
}

function handleLogout() {
    token = null;
    localStorage.removeItem('todo_token');
    updateAuthState();
    showToast('Đã đăng xuất', 'success');
}

// Event Listeners
function setupEventListeners() {
    // Auth Tabs
    tabLogin.addEventListener('click', () => {
        tabLogin.classList.add('active');
        tabRegister.classList.remove('active');
        loginForm.style.display = 'block';
        registerForm.style.display = 'none';
    });

    tabRegister.addEventListener('click', () => {
        tabRegister.classList.add('active');
        tabLogin.classList.remove('active');
        registerForm.style.display = 'block';
        loginForm.style.display = 'none';
    });

    // Auth Forms
    loginForm.addEventListener('submit', handleLogin);
    registerForm.addEventListener('submit', handleRegister);
    logoutBtn.addEventListener('click', handleLogout);

    // Todo Actions
    addTodoForm.addEventListener('submit', handleAddTodo);
    searchInput.addEventListener('input', debounce(handleSearch, 500));
    statusFilter.addEventListener('change', handleFilterChange);
    sortOrder.addEventListener('change', handleSortChange);
    refreshBtn.addEventListener('click', handleRefresh);
}

// API Functions - Auth
async function handleLogin(e) {
    e.preventDefault();
    const email = document.getElementById('loginEmail').value;
    const password = document.getElementById('loginPassword').value;

    try {
        const formData = new FormData();
        formData.append('username', email);
        formData.append('password', password);

        const response = await fetch(`${API_BASE_URL}/auth/login`, {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Đăng nhập thất bại');
        }

        const data = await response.json();
        token = data.access_token;
        localStorage.setItem('todo_token', token);
        updateAuthState();
        showToast('Đăng nhập thành công!', 'success');
    } catch (error) {
        showToast(error.message, 'error');
    }
}

async function handleRegister(e) {
    e.preventDefault();
    const email = document.getElementById('registerEmail').value;
    const password = document.getElementById('registerPassword').value;

    try {
        const response = await fetch(`${API_BASE_URL}/auth/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Đăng ký thất bại');
        }

        showToast('Đăng ký thành công! Hãy đăng nhập.', 'success');
        tabLogin.click(); // Switch to login tab
    } catch (error) {
        showToast(error.message, 'error');
    }
}

// API Functions - Todos (With Token)
async function fetchTodos() {
    const params = new URLSearchParams();
    if (currentSearch) params.append('q', currentSearch);
    if (currentFilter === 'completed') params.append('is_done', 'true');
    else if (currentFilter === 'pending') params.append('is_done', 'false');

    params.append('sort', currentSort);
    params.append('limit', '100');
    params.append('offset', '0');

    const response = await fetch(`${API_BASE_URL}/todos?${params.toString()}`, {
        headers: { 'Authorization': `Bearer ${token}` }
    });

    if (response.status === 401) {
        handleLogout();
        throw new Error('Phiên làm việc hết hạn');
    }

    if (!response.ok) throw new Error('Không thể tải danh sách');
    const data = await response.json();
    return data;
}

// Handler Functions
async function handleAddTodo(e) {
    e.preventDefault();
    const title = todoInput.value.trim();
    if (!title) return;

    try {
        const response = await fetch(`${API_BASE_URL}/todos`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ title }),
        });

        if (!response.ok) throw new Error('Không thể thêm công việc');

        todoInput.value = '';
        showToast('Đã thêm công việc!', 'success');
        await loadTodos();
    } catch (error) {
        showToast(error.message, 'error');
    }
}

async function handleToggleTodo(id, currentStatus) {
    try {
        const response = await fetch(`${API_BASE_URL}/todos/${id}`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ is_done: !currentStatus }),
        });

        if (!response.ok) throw new Error('Lỗi cập nhật');
        await loadTodos();
    } catch (error) {
        showToast(error.message, 'error');
    }
}

async function handleDeleteTodo(id) {
    if (!confirm('Xóa công việc này?')) return;
    try {
        const response = await fetch(`${API_BASE_URL}/todos/${id}`, {
            method: 'DELETE',
            headers: { 'Authorization': `Bearer ${token}` }
        });
        if (!response.ok) throw new Error('Lỗi xóa');
        showToast('Đã xóa', 'success');
        await loadTodos();
    } catch (error) {
        showToast(error.message, 'error');
    }
}

// UI Helpers
async function loadTodos(isInitial = false) {
    if (!token) return;
    showLoading(true);
    try {
        const data = await fetchTodos();
        todos = data.items;
        renderTodos();
        updateStats(data.total);
    } catch (error) {
        // Don't show toast for initial 401 as it's handled by updateAuthState
        if (!isInitial) {
            showToast(error.message, 'error');
        }
    } finally {
        showLoading(false);
    }
}

function renderTodos() {
    todoList.innerHTML = '';
    if (todos.length === 0) {
        emptyState.style.display = 'block';
        return;
    }
    emptyState.style.display = 'none';
    todos.forEach(todo => {
        const li = createTodoElement(todo);
        todoList.appendChild(li);
    });
}

function createTodoElement(todo) {
    const li = document.createElement('li');
    li.className = `todo-item ${todo.is_done ? 'completed' : ''}`;
    const date = new Date(todo.created_at).toLocaleString('vi-VN');

    li.innerHTML = `
        <div class="todo-checkbox ${todo.is_done ? 'checked' : ''}"></div>
        <div class="todo-content">
            <div class="todo-title">${escapeHtml(todo.title)}</div>
            <div class="todo-date">${date}</div>
        </div>
        <div class="todo-actions">
            <button class="btn-icon-only btn-delete" title="Xóa">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M3 6h18M19 6v14a2 2 0 01-2 2H7a2 2 0 01-2-2V6m3 0V4a2 2 0 012-2h4a2 2 0 012 2v2"></path>
                </svg>
            </button>
        </div>
    `;

    li.querySelector('.todo-checkbox').onclick = () => handleToggleTodo(todo.id, todo.is_done);
    li.querySelector('.btn-delete').onclick = () => handleDeleteTodo(todo.id);
    return li;
}

function updateStats(total) {
    totalCount.textContent = total;
    completedCount.textContent = todos.filter(t => t.is_done).length;
}

function showLoading(show) {
    loadingSpinner.style.display = show ? 'block' : 'none';
    todoList.style.display = show ? 'none' : 'block';
}

function showToast(msg, type) {
    const toast = document.getElementById('toast');
    toast.textContent = msg;
    toast.className = `toast ${type} show`;
    setTimeout(() => toast.classList.remove('show'), 3000);
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function debounce(func, wait) {
    let timeout;
    return (...args) => {
        clearTimeout(timeout);
        timeout = setTimeout(() => func(...args), wait);
    };
}

function handleSearch(e) { currentSearch = e.target.value; loadTodos(); }
function handleFilterChange(e) { currentFilter = e.target.value; loadTodos(); }
function handleSortChange(e) { currentSort = e.target.value; loadTodos(); }
function handleRefresh() { loadTodos(); }
