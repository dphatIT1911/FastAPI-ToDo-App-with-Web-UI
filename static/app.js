// API Configuration
const API_BASE_URL = 'http://localhost:8000/api/v1';

// State
let todos = [];
let currentFilter = 'all';
let currentSearch = '';
let currentSort = '-created_at';

// DOM Elements
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
const pendingCount = document.getElementById('pendingCount');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    loadTodos();
    setupEventListeners();
});

// Event Listeners
function setupEventListeners() {
    addTodoForm.addEventListener('submit', handleAddTodo);
    searchInput.addEventListener('input', debounce(handleSearch, 500));
    statusFilter.addEventListener('change', handleFilterChange);
    sortOrder.addEventListener('change', handleSortChange);
    refreshBtn.addEventListener('click', handleRefresh);
}

// API Functions
async function fetchTodos() {
    const params = new URLSearchParams();
    
    if (currentSearch) {
        params.append('q', currentSearch);
    }
    
    if (currentFilter === 'completed') {
        params.append('is_done', 'true');
    } else if (currentFilter === 'pending') {
        params.append('is_done', 'false');
    }
    
    params.append('sort', currentSort);
    params.append('limit', '100');
    params.append('offset', '0');
    
    const response = await fetch(`${API_BASE_URL}/todos?${params.toString()}`);
    if (!response.ok) throw new Error('Failed to fetch todos');
    
    const data = await response.json();
    return data.items;
}

async function createTodo(title) {
    const response = await fetch(`${API_BASE_URL}/todos`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ title }),
    });
    
    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Failed to create todo');
    }
    
    return response.json();
}

async function updateTodo(id, data) {
    const response = await fetch(`${API_BASE_URL}/todos/${id}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    });
    
    if (!response.ok) throw new Error('Failed to update todo');
    return response.json();
}

async function deleteTodo(id) {
    const response = await fetch(`${API_BASE_URL}/todos/${id}`, {
        method: 'DELETE',
    });
    
    if (!response.ok) throw new Error('Failed to delete todo');
    return response.json();
}

// Handler Functions
async function handleAddTodo(e) {
    e.preventDefault();
    
    const title = todoInput.value.trim();
    if (!title || title.length < 3) {
        showToast('Tiêu đề phải có ít nhất 3 ký tự', 'error');
        return;
    }
    
    try {
        await createTodo(title);
        todoInput.value = '';
        showToast('Đã thêm công việc mới!', 'success');
        await loadTodos();
    } catch (error) {
        showToast(error.message, 'error');
    }
}

async function handleToggleTodo(id, currentStatus) {
    try {
        await updateTodo(id, { is_done: !currentStatus });
        await loadTodos();
        showToast(currentStatus ? 'Đã đánh dấu chưa hoàn thành' : 'Đã hoàn thành!', 'success');
    } catch (error) {
        showToast(error.message, 'error');
    }
}

async function handleDeleteTodo(id) {
    if (!confirm('Bạn có chắc muốn xóa công việc này?')) return;
    
    try {
        await deleteTodo(id);
        showToast('Đã xóa công việc', 'success');
        await loadTodos();
    } catch (error) {
        showToast(error.message, 'error');
    }
}

function handleSearch(e) {
    currentSearch = e.target.value.trim();
    loadTodos();
}

function handleFilterChange(e) {
    currentFilter = e.target.value;
    loadTodos();
}

function handleSortChange(e) {
    currentSort = e.target.value;
    loadTodos();
}

function handleRefresh() {
    refreshBtn.classList.add('rotating');
    loadTodos().finally(() => {
        setTimeout(() => {
            refreshBtn.classList.remove('rotating');
        }, 500);
    });
}

// UI Functions
async function loadTodos() {
    showLoading(true);
    try {
        todos = await fetchTodos();
        renderTodos();
        updateStats();
    } catch (error) {
        showToast('Lỗi khi tải dữ liệu: ' + error.message, 'error');
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
    
    const createdDate = new Date(todo.created_at).toLocaleString('vi-VN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
    });
    
    li.innerHTML = `
        <div class="todo-checkbox ${todo.is_done ? 'checked' : ''}" data-id="${todo.id}" data-status="${todo.is_done}"></div>
        <div class="todo-content">
            <div class="todo-title">${escapeHtml(todo.title)}</div>
            <div class="todo-date">${createdDate}</div>
        </div>
        <div class="todo-actions">
            <button class="btn-icon-only btn-delete" data-id="${todo.id}" title="Xóa">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M3 6h18M19 6v14a2 2 0 01-2 2H7a2 2 0 01-2-2V6m3 0V4a2 2 0 012-2h4a2 2 0 012 2v2"></path>
                </svg>
            </button>
        </div>
    `;
    
    // Add event listeners
    const checkbox = li.querySelector('.todo-checkbox');
    checkbox.addEventListener('click', () => handleToggleTodo(todo.id, todo.is_done));
    
    const deleteBtn = li.querySelector('.btn-delete');
    deleteBtn.addEventListener('click', () => handleDeleteTodo(todo.id));
    
    return li;
}

function updateStats() {
    const total = todos.length;
    const completed = todos.filter(t => t.is_done).length;
    const pending = total - completed;
    
    totalCount.textContent = total;
    completedCount.textContent = completed;
    pendingCount.textContent = pending;
}

function showLoading(show) {
    loadingSpinner.style.display = show ? 'block' : 'none';
    todoList.style.display = show ? 'none' : 'block';
}

function showToast(message, type = 'success') {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.className = `toast ${type} show`;
    
    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}

// Utility Functions
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Add rotation animation for refresh button
const style = document.createElement('style');
style.textContent = `
    @keyframes rotate {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    .rotating svg {
        animation: rotate 0.5s linear;
    }
`;
document.head.appendChild(style);
