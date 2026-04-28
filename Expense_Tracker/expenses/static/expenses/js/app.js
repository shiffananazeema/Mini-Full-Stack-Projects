function getJsonScriptValue(id) {
    const node = document.getElementById(id);
    return node ? JSON.parse(node.textContent) : [];
}

function drawEmptyState(ctx, width, height, message) {
    ctx.clearRect(0, 0, width, height);
    ctx.fillStyle = "#74685f";
    ctx.font = "16px Georgia";
    ctx.fillText(message, 24, height / 2);
}

function drawPieChart() {
    const canvas = document.getElementById("categoryPieChart");
    if (!canvas) {
        return;
    }

    const labels = getJsonScriptValue("category-labels");
    const values = getJsonScriptValue("category-values");
    const ctx = canvas.getContext("2d");
    const width = canvas.parentElement.clientWidth - 24;
    const height = 260;
    const pixelRatio = window.devicePixelRatio || 1;
    const total = values.reduce((sum, value) => sum + value, 0);
    const colors = ["#c85c38", "#2f6f64", "#e3a54c", "#7851a9", "#cc6d7a", "#5e748c", "#8f855f"];
    const centerX = width / 2;
    const centerY = height / 2;
    const radius = Math.min(width, height) * 0.34;

    canvas.width = width * pixelRatio;
    canvas.height = height * pixelRatio;
    canvas.style.width = `${width}px`;
    canvas.style.height = `${height}px`;
    ctx.setTransform(pixelRatio, 0, 0, pixelRatio, 0, 0);

    if (!labels.length || total === 0) {
        drawEmptyState(ctx, width, height, "Add expenses to see the pie chart.");
        return;
    }

    ctx.clearRect(0, 0, width, height);

    let startAngle = -Math.PI / 2;
    values.forEach((value, index) => {
        const sliceAngle = (value / total) * Math.PI * 2;

        ctx.beginPath();
        ctx.moveTo(centerX, centerY);
        ctx.arc(centerX, centerY, radius, startAngle, startAngle + sliceAngle);
        ctx.closePath();
        ctx.fillStyle = colors[index % colors.length];
        ctx.fill();
        ctx.strokeStyle = "#fffdf8";
        ctx.lineWidth = 3;
        ctx.stroke();

        startAngle += sliceAngle;
    });
}

function setModalVisibility(modal, visible) {
    if (!modal) {
        return;
    }

    modal.classList.toggle("is-visible", visible);
    modal.setAttribute("aria-hidden", visible ? "false" : "true");
}

function setupExpenseModals() {
    const addModal = document.getElementById("expenseModal");
    const editModal = document.getElementById("editExpenseModal");
    const editForm = document.getElementById("editExpenseForm");

    const editTitle = document.getElementById("id_edit-title");
    const editCategory = document.getElementById("id_edit-category");
    const editAmount = document.getElementById("id_edit-amount");
    const editDate = document.getElementById("id_edit-expense_date");

    document.querySelectorAll("[data-open-modal]").forEach((button) => {
        button.addEventListener("click", () => {
            setModalVisibility(addModal, true);
            setModalVisibility(editModal, false);
        });
    });

    document.querySelectorAll("[data-open-edit-modal]").forEach((button) => {
        button.addEventListener("click", () => {
            if (editForm) {
                editForm.action = `/edit/${button.dataset.expenseId}/`;
            }
            if (editTitle) {
                editTitle.value = button.dataset.title || "";
            }
            if (editCategory) {
                editCategory.value = button.dataset.category || "";
            }
            if (editAmount) {
                editAmount.value = button.dataset.amount || "";
            }
            if (editDate) {
                editDate.value = button.dataset.expenseDate || "";
            }

            setModalVisibility(addModal, false);
            setModalVisibility(editModal, true);
        });
    });

    document.querySelectorAll("[data-close-modal]").forEach((button) => {
        button.addEventListener("click", () => {
            setModalVisibility(addModal, false);
            setModalVisibility(editModal, false);
        });
    });

    [addModal, editModal].forEach((modal) => {
        if (!modal) {
            return;
        }

        modal.addEventListener("click", (event) => {
            if (event.target === modal) {
                setModalVisibility(modal, false);
            }
        });
    });

    window.addEventListener("keydown", (event) => {
        if (event.key === "Escape") {
            setModalVisibility(addModal, false);
            setModalVisibility(editModal, false);
        }
    });
}

window.addEventListener("load", () => {
    drawPieChart();
    setupExpenseModals();
});

window.addEventListener("resize", drawPieChart);
