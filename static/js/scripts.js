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
  });

  document.getElementById('guestsLink').addEventListener('click', function (e) {
    e.preventDefault();
    loadGuestsContent();
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
  fetch('/auth/members')
    .then(response => response.text())
    .then(data => {
      document.getElementById('main-container').innerHTML = data;
    })
    .catch(error => console.error('Error:', error));
}

function loadGuestsContent() {
  fetch('/auth/guests')
    .then(response => response.text())
    .then((data) => {
      document.getElementById('main-container').innerHTML = data;
    })
    .catch((error) => {
      console.error('Error:', error);
    });
}

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

// Fonction pour ouvrir le modal d'édition et pré-remplir les champs avec les valeurs du membre sélectionné
function openEditModal(rowIndex) {
  // Récupérer les valeurs du membre à partir du tableau
  // var rowData = /* Code pour récupérer les valeurs du tableau en fonction de l'index de ligne (rowIndex) */

  // // Pré-remplir les champs du formulaire avec les valeurs du membre
  // document.getElementById("editFirstName").value = rowData.firstName;
  // document.getElementById("editLastName").value = rowData.lastName;
  // document.getElementById("editPhone").value = rowData.phone;
  // document.getElementById("editEmail").value = rowData.email;
  // document.getElementById("editIsPayed").value = rowData.isPayed;

  // // Stocker l'index de ligne dans un champ caché pour référence ultérieure
  // document.getElementById("editRowIndex").value = rowIndex;

  // Ouvrir le modal d'édition
  document.getElementById("editModal").style.display = "block";
}


function closeEditModal() {
  document.getElementById("editModal").style.display = "none";
}












