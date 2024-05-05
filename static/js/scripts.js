// SIDEBAR TOGGLE

let sidebarOpen = false;
const sidebar = document.getElementById('sidebar');

function openSidebar() {
  if (!sidebarOpen) {
    sidebar.classList.add('sidebar-responsive');
    sidebarOpen = true;
  }
}

function closeSidebar() {
  if (sidebarOpen) {
    sidebar.classList.remove('sidebar-responsive');
    sidebarOpen = false;
  }
}

// ---------- CHARTS ----------

// BAR CHART
const barChartOptions = {
  series: [
    {
      data: [10, 8, 6, 4, 2],
      name: 'Products',
    },
  ],
  chart: {
    type: 'bar',
    background: 'transparent',
    height: 350,
    toolbar: {
      show: false,
    },
  },
  colors: ['#2962ff', '#d50000', '#2e7d32', '#ff6d00', '#583cb3'],
  plotOptions: {
    bar: {
      distributed: true,
      borderRadius: 4,
      horizontal: false,
      columnWidth: '40%',
    },
  },
  dataLabels: {
    enabled: false,
  },
  fill: {
    opacity: 1,
  },
  grid: {
    borderColor: '#55596e',
    yaxis: {
      lines: {
        show: true,
      },
    },
    xaxis: {
      lines: {
        show: true,
      },
    },
  },
  legend: {
    labels: {
      colors: '#f5f7ff',
    },
    show: true,
    position: 'top',
  },
  stroke: {
    colors: ['transparent'],
    show: true,
    width: 2,
  },
  tooltip: {
    shared: true,
    intersect: false,
    theme: 'dark',
  },
  xaxis: {
    categories: ['Laptop', 'Phone', 'Monitor', 'Headphones', 'Camera'],
    title: {
      style: {
        color: '#f5f7ff',
      },
    },
    axisBorder: {
      show: true,
      color: '#55596e',
    },
    axisTicks: {
      show: true,
      color: '#55596e',
    },
    labels: {
      style: {
        colors: '#f5f7ff',
      },
    },
  },
  yaxis: {
    title: {
      text: 'Count',
      style: {
        color: '#f5f7ff',
      },
    },
    axisBorder: {
      color: '#55596e',
      show: true,
    },
    axisTicks: {
      color: '#55596e',
      show: true,
    },
    labels: {
      style: {
        colors: '#f5f7ff',
      },
    },
  },
};

const barChart = new ApexCharts(
  document.querySelector('#bar-chart'),
  barChartOptions
);
barChart.render();

// AREA CHART
const areaChartOptions = {
  series: [
    {
      name: 'Purchase Orders',
      data: [31, 40, 28, 51, 42, 109, 100],
    },
    {
      name: 'Sales Orders',
      data: [11, 32, 45, 32, 34, 52, 41],
    },
  ],
  chart: {
    type: 'area',
    background: 'transparent',
    height: 350,
    stacked: false,
    toolbar: {
      show: false,
    },
  },
  colors: ['#00ab57', '#d50000'],
  labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul'],
  dataLabels: {
    enabled: false,
  },
  fill: {
    gradient: {
      opacityFrom: 0.4,
      opacityTo: 0.1,
      shadeIntensity: 1,
      stops: [0, 100],
      type: 'vertical',
    },
    type: 'gradient',
  },
  grid: {
    borderColor: '#55596e',
    yaxis: {
      lines: {
        show: true,
      },
    },
    xaxis: {
      lines: {
        show: true,
      },
    },
  },
  legend: {
    labels: {
      colors: '#f5f7ff',
    },
    show: true,
    position: 'top',
  },
  markers: {
    size: 6,
    strokeColors: '#1b2635',
    strokeWidth: 3,
  },
  stroke: {
    curve: 'smooth',
  },
  xaxis: {
    axisBorder: {
      color: '#55596e',
      show: true,
    },
    axisTicks: {
      color: '#55596e',
      show: true,
    },
    labels: {
      offsetY: 5,
      style: {
        colors: '#f5f7ff',
      },
    },
  },
  yaxis: [
    {
      title: {
        text: 'Purchase Orders',
        style: {
          color: '#f5f7ff',
        },
      },
      labels: {
        style: {
          colors: ['#f5f7ff'],
        },
      },
    },
    {
      opposite: true,
      title: {
        text: 'Sales Orders',
        style: {
          color: '#f5f7ff',
        },
      },
      labels: {
        style: {
          colors: ['#f5f7ff'],
        },
      },
    },
  ],
  tooltip: {
    shared: true,
    intersect: false,
    theme: 'dark',
  },
};

const areaChart = new ApexCharts(
  document.querySelector('#area-chart'),
  areaChartOptions
);
areaChart.render();


document.addEventListener("DOMContentLoaded", function () {

  

  

  document.getElementById('membersLink').addEventListener('click', function (e) {
    e.preventDefault();
    loadMembersContent();
    loadMembersData();
  });

  document.getElementById('guestsLink').addEventListener('click', function (e) {
    e.preventDefault();
    loadGuestsContent();
    loadGuestsData();
  });

  document.getElementById('parkingLink').addEventListener('click', function (e) {
    e.preventDefault();
    loadParkingContent();
  });

  document.getElementById('tarifsLink').addEventListener('click', function (e) {
    e.preventDefault();
    loadTarifsContent();
  });

  document.getElementById('cameraLink').addEventListener('click', function (e) {
    e.preventDefault();
    loadCameraContent();
  });


  
  
});





function loadMembersContent() {
  console.log("Loading members...");
  fetch('/auth/members')
    .then(response => response.text())
    .then(data => {
      console.log("Data received:", data);  // Ajout pour déboguer et voir les données reçues
      document.getElementById('main-container').innerHTML = data;
    })
    .catch(error => console.error('Error:', error));
}

function loadGuestsContent() {
  console.log("Loading guests...");
  fetch('/auth/guests')
    .then(response => response.text())
    .then(data => {
      console.log("Data received:", data);  // Ajout pour déboguer et voir les données reçues
      document.getElementById('main-container').innerHTML = data;
    })
    .catch(error => console.error('Error:', error));
}

function loadGuestsData() {
    fetch('/auth/guests/data')
        .then(response => response.json())
        .then(data => {
            const tbody = document.getElementById('guests-tbody');
            tbody.innerHTML = ''; // Clear previous data
            data.forEach(guest => {
                const row = `<tr>
                     <td>${guest.Code}</td>
                     <td>${guest.PlateNumber}</td>
                     <td>${guest.EntryDate}</td>
                     <td>${guest.ExitDate}</td>
                     <td>${guest.PriceToPay}</td>
                </tr>`;
                tbody.innerHTML += row;
            });
        })
        .catch(error => {
            console.error('Error loading guest data:', error);
            alert('Failed to load guest data.');
        });
}

function loadMembersData() {
    fetch('/auth/members/data')
        .then(response => response.json())
        .then(data => {
            const tbody = document.getElementById('members-tbody');
            tbody.innerHTML = '';
            data.forEach(member => {
                const isPayedText = member.isPayed ? 'Yes' : 'No';
                const row = `<tr>
                    <td>${member.FirstName}</td>
                    <td>${member.LastName}</td>
                    <td>${member.Phone}</td>
                    <td>${member.Email}</td>
                    <td>${member.Matricules || 'No plates registered'}</td>
                    <td>${isPayedText}</td>
                    <td>
                        <button onclick="openEditModal(this)" class="edit-btn" data-id="${member.ID}"><i class="fas fa-edit"></i></button>
                        <button onclick="deleteMember(this)" class="delete-btn" data-id="${member.ID}"><i class="fas fa-trash-alt"></i></button>

                    </td>
                </tr>`;
                tbody.innerHTML += row;
            });
        })
        .catch(error => {
            console.error('Error loading member data:', error);
            alert('Failed to load member data.');
        });
}

function deleteMember(button) {
  const memberId = button.getAttribute('data-id');
  console.log('Attempting to delete member with ID:', memberId);  // Debugging output

  if (!confirm('Are you sure you want to delete this member?')) {
    return;
  }

  fetch(`/auth/delete_member/${memberId}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    }
  })
  .then(response => {
    console.log('Response status:', response.status); // Debugging output
    if (!response.ok) {
      throw new Error(`Failed to delete member with status: ${response.status}`);
    }
    return response.json();
  })
  .then(data => {
    if (data.error) {
      alert(data.error);
    } else {
      alert('Member deleted successfully!');
      button.closest('tr').remove();  // Remove the row from the table
    }
  })
  .catch(error => {
    console.error('Error:', error);
    alert('Failed to delete member: ' + error.message);
  });
}


// Edit Member
// affiche les données dans le formulaire
function openEditModal(button) {
  const memberId = button.getAttribute('data-id');
  const row = button.closest('tr');
  const cells = row.getElementsByTagName('td');

  document.getElementById('editFirstName').value = cells[0].textContent.trim();
  document.getElementById('editLastName').value = cells[1].textContent.trim();
  document.getElementById('editPhone').value = cells[2].textContent.trim();
  document.getElementById('editEmail').value = cells[3].textContent.trim();
  // Adjust for 'Is Payed' select option value setup
  document.getElementById('editIsPayed').value = cells[5].textContent.trim() === 'Yes' ? 'yes' : 'no';
  document.getElementById('editMemberId').value = memberId;

  var modal = document.getElementById('editModal');
  modal.style.display = 'block';
}


function editMember() {
  const memberId = document.getElementById('editMemberId').value;
  const data = {
    firstName: document.getElementById('editFirstName').value,
    lastName: document.getElementById('editLastName').value,
    phone: document.getElementById('editPhone').value,
    email: document.getElementById('editEmail').value,
    isPayed: document.getElementById('editIsPayed').value === 'yes' ? 1 : 0
  };

  fetch(`/auth/update_member/${memberId}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
  })
  .then(response => response.json())
  .then(data => {
    if (data.status === 'error') {
      alert(data.message);
    } else {
      alert('Member updated successfully!');
      loadMembersData(); // Reload data to reflect changes
      closeEditModal(); // Close the modal after update
    }
  })
  .catch(error => {
    console.error('Error:', error);
    alert('Failed to update member: ' + error.message);
  });
}

// Ensure the edit form submission is hooked correctly
document.getElementById('editForm').addEventListener('submit', function(event) {
  event.preventDefault(); // Prevent the default form submission

  const memberId = document.getElementById('editMemberId').value;
  const data = {
    firstName: document.getElementById('editFirstName').value,
    lastName: document.getElementById('editLastName').value,
    phone: document.getElementById('editPhone').value,
    email: document.getElementById('editEmail').value,
    isPayed: document.getElementById('editIsPayed').value === 'yes' ? 1 : 0
  };

  fetch(`/auth/update_member/${memberId}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
  })
  .then(response => response.json())
  .then(data => {
    if (data.status === 'error') {
      alert(data.message);
    } else {
      alert('Member updated successfully!');
      loadMembersData(); // Reload data to reflect changes
      closeEditModal(); // Close the modal after update
    }
  })
  .catch(error => {
    console.error('Error:', error);
    alert('Failed to update member: ' + error.message);
  });
});




// Hook this function to your form's submit event
document.getElementById('editForm').addEventListener('submit', function(event) {
  event.preventDefault(); // Prevent the default form submission
  editMember();
});

function loadParkingContent() {
  fetch('/auth/parking')
    .then(response => response.text())
    .then((data) => {
      document.getElementById('main-container').innerHTML = data;
    })
    .catch((error) => {
      console.error('Error:', error);
    });

}

function loadTarifsContent() {
  fetch('/auth/tarifs')
    .then(response => response.text())
    .then((data) => {
      document.getElementById('main-container').innerHTML = data;
    })
    .catch((error) => {
      console.error('Error:', error);
    });

}

function loadCameraContent() {
  fetch('/auth/camera')
    .then(response => response.text())
    .then((data) => {
      document.getElementById('main-container').innerHTML = data;
    })
    .catch((error) => {
      console.error('Error:', error);
    });


}

function openModal() {
  var modal = document.getElementById("myModal");
  modal.style.display = "block";
}

function closeModal() {
  var modal = document.getElementById("myModal");
  modal.style.display = "none";
}



function closeEditModal() {
  document.getElementById("editModal").style.display = "none";
}
















