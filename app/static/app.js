const apiUrl = "http://localhost:8001";  // Change this if running FastAPI on another port

// DOM Elements
const taskTitleInput = document.getElementById("task-title");
const taskDescInput = document.getElementById("task-desc");
const createTaskBtn = document.getElementById("create-task-btn");
const tasksContainer = document.getElementById("tasks-container");

// Fetch and display all tasks on page load
window.onload = () => {
    fetchTasks();
}

// Create a new task
createTaskBtn.addEventListener("click", async () => {
    const title = taskTitleInput.value.trim();
    const description = taskDescInput.value.trim();

    if (!title) {
        alert("Please enter a task title");
        return;
    }

    const newTask = {
        title: title,
        description: description
    };

    const response = await fetch(`${apiUrl}/tasks/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(newTask)
    });

    if (response.ok) {
        fetchTasks();  // Refresh task list
        taskTitleInput.value = "";  // Clear form
        taskDescInput.value = "";
    }
});

// Fetch tasks from the API and display them
async function fetchTasks() {
    const response = await fetch(`${apiUrl}/tasks/`);
    const tasks = await response.json();

    renderTasks(tasks);
    tasksContainer.innerHTML = "";  // Clear current tasks

    tasks.forEach(task => {
        const taskElement = createTaskElement(task);
        tasksContainer.appendChild(taskElement);
    });
}

// Render tasks based on status filter
function renderTasks(tasks) {
    const taskList = document.getElementById('tasks-list');
    taskList.innerHTML = '';

    const selectedStatus = document.getElementById('status-filter').value;

    tasks
        .filter(task => selectedStatus === 'all' || task.status === selectedStatus)
        .forEach(task => {
            const taskElement = document.createElement('div');
            taskElement.classList.add('task');
            taskElement.classList.add(task.status.toLowerCase().replace(' ', '-'));  // Add class for styling

            taskElement.innerHTML = `
                <h3>${task.title}</h3>
                <p>${task.description}</p>
                <p>Status: ${task.status}</p>
                <button onclick="updateTaskStatus(${task.id}, 'Doing')">Doing</button>
                <button onclick="updateTaskStatus(${task.id}, 'Done')">Done</button>
                <button onclick="deleteTask(${task.id})">Delete</button>
            `;
            taskList.appendChild(taskElement);
        });
}

// Create the task DOM element
function createTaskElement(task) {
    const taskDiv = document.createElement("div");
    taskDiv.classList.add("task");

    // Assign a class based on the task status
    if (task.status === "ToDo") {
        taskDiv.classList.add("todo");
    } else if (task.status === "Doing") {
        taskDiv.classList.add("doing");
    } else if (task.status === "Done") {
        taskDiv.classList.add("done");
    }

    const taskTitle = document.createElement("h3");
    taskTitle.textContent = task.title;

    const taskDesc = document.createElement("p");
    taskDesc.textContent = task.description || "No description";

    const taskStatus = document.createElement("p");
    taskStatus.textContent = `Status: ${task.status}`;

    const taskActions = document.createElement("div");

    const moveToDoingBtn = document.createElement("button");
    moveToDoingBtn.textContent = "Move to Doing";
    moveToDoingBtn.onclick = () => updateTaskStatus(task.id, "Doing");

    const moveToDoneBtn = document.createElement("button");
    moveToDoneBtn.textContent = "Move to Done";
    moveToDoneBtn.onclick = () => updateTaskStatus(task.id, "Done");

    const deleteTaskBtn = document.createElement("button");
    deleteTaskBtn.textContent = "Delete Task";
    deleteTaskBtn.onclick = () => deleteTask(task.id);

    taskActions.appendChild(moveToDoingBtn);
    taskActions.appendChild(moveToDoneBtn);
    taskActions.appendChild(deleteTaskBtn);

    taskDiv.appendChild(taskTitle);
    taskDiv.appendChild(taskDesc);
    taskDiv.appendChild(taskStatus);
    taskDiv.appendChild(taskActions);

    return taskDiv;
}

// Update task status
async function updateTaskStatus(taskId, status) {
    const response = await fetch(`${apiUrl}/tasks/${taskId}/status`, {
        method: "PATCH",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ status })
    });

    if (response.ok) {
        fetchTasks();  // Refresh task list
    }
}

// Delete a task
async function deleteTask(taskId) {
    const response = await fetch(`${apiUrl}/tasks/${taskId}`, {
        method: "DELETE"
    });

    if (response.ok) {
        fetchTasks();  // Refresh task list
    }
}

// Filter tasks based on the selected status
function filterTasks() {
    fetchTasks();
}
