function openAddModal() {
  document.getElementById("modalTitle").innerText = "Add New Item";
  document.getElementById("modalSubmitBtn").innerText = "Add";
  document.getElementById("modalForm").action = "/add/";

  document.getElementById("modalTitleInput").value = "";
  document.getElementById("modalContentInput").value = "";
  document.getElementById("modalTypeInput").value = "task";
  document.getElementById("hiddenTypeInput").value = "task";
  document.getElementById("modalPriorityInput").value = "low";
  document.getElementById("modalDueDateInput").value = "";

  toggleTaskFields();
  document.getElementById("taskModal").style.display = "flex";
}

function openEditModal(id, title, content, itemType, priority, dueDate) {
  document.getElementById("modalTitle").innerText = "Edit Item";
  document.getElementById("modalSubmitBtn").innerText = "Update";
  document.getElementById("modalForm").action = `/edit/${id}/`;

  document.getElementById("modalTitleInput").value = title || "";
  document.getElementById("modalContentInput").value = content || "";
  document.getElementById("modalTypeInput").value = itemType || "task";
  document.getElementById("hiddenTypeInput").value = itemType || "task";
  document.getElementById("modalPriorityInput").value = priority || "low";
  document.getElementById("modalDueDateInput").value = dueDate || "";

  toggleTaskFields();
  document.getElementById("taskModal").style.display = "flex";
}

function handleEditClick(button) {
  const id = button.dataset.id;
  const title = button.dataset.title;
  const content = button.dataset.content;
  const itemType = button.dataset.itemType;
  const priority = button.dataset.priority;
  const dueDate = button.dataset.dueDate;

  openEditModal(id, title, content, itemType, priority, dueDate);
}

function closeModal() {
  document.getElementById("taskModal").style.display = "none";
}

function toggleTaskFields() {
  const type = document.getElementById("modalTypeInput").value;
  const taskFields = document.getElementById("taskFields");
  document.getElementById("hiddenTypeInput").value = type;

  if (type === "note") {
    taskFields.style.display = "none";
  } else {
    taskFields.style.display = "flex";
  }
}

window.onclick = function (event) {
  const modal = document.getElementById("taskModal");
  if (event.target === modal) {
    closeModal();
  }
};
