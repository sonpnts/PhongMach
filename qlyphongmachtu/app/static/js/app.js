function addBook() {
    let desc = document.getElementById('descId');
    let date = document.getElementById('dateId');
    let selectElement = document.getElementById('timeId');
    let timeId = selectElement.value;
    if (desc !== null) {
        fetch('/api/booking-form', {
            method: 'post',
            body: JSON.stringify({
                'date': date.value,
                'desc': desc.value,
                'time_id': timeId
            }),
            headers: {
                'Content-Type': "application/json"
            }
        }).then(function (res) {
            return res.json();

        }).then(function (data) {
            if (data.status == 201) {
                alert('Đặt lịch hành công')
            } else if (data.status == 404) {
                alert('Đặt lịch thất bại')
            }
        })
    }
}


function lenlich(id) {
    checkPatientCount();
    fetch('/len-ds', {
        method: "post",
        body: JSON.stringify({
            "id": id,
        }),
        headers: {
            'Content-Type': "application/json"
        }
    }).then(function (res) {
        return res.json();

    }).then(function (data) {
        window.location.reload();
        alert('Đã thêm thành công bệnh nhân!');
    })
}


function lenphieukham(id) {
    fetch('/len-pk', {
        method: "post",
        body: JSON.stringify({
            "id": id,
        }),
        headers: {
            'Content-Type': "application/json"
        }
    }).then(function (res) {
        return res.json();

    }).then(function (data){
        window.location.href = "/phieukham" ;
    });
}


function checkPatientCount() {
    fetch('/api/check-patient-count')
        .then(response => response.json())
        .then(data => {
            if (data.patients_today >= data.quantity_patient) {
                // alert('Đã đủ 40 bệnh nhân, không thể đăng ký thêm!');
                document.getElementById('message-container').innerText = 'Đã đủ bệnh nhân, không thể đăng ký thêm!';
                var buttons = document.querySelectorAll('button.book-btn');
                buttons.forEach(button => {
                    button.disabled = true;
                });
                var messageContainer = document.getElementById('message-container');
                messageContainer.innerText = message;
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

window.onload = function () {
    checkPatientCount();
};




// function addReceipt() {
//     let examines_price = document.getElementById('examinespriceId').value();
//     let total = document.getElementById('totalId').value();
//     let patient_id = document.getElementById('p_id').value();
//     if (examines_price !== null) {
//         fetch('/api/receipt-form', {
//             method: 'post',
//             body: JSON.stringify({
//                 'examines_price': examines_price,
//                 'total': total,
//                 'patient_id': patient_id
//             }),
//             headers: {
//                 'Content-Type': "application/json"
//             }
//         }).then(function (res) {
//             return res.json();
//
//         }).then(function (data) {
//             if (data.status == 201) {
//                 alert('Thanh toán thành công')
//             } else if (data.status == 404) {
//                 alert('Thanh toán thất bại')
//             }
//         })
//     }
// }


function thanhToan(id, tongTien) {
    // let tienThuoc = document.getElementById('tienThuoc');
    // let tongTien = document.getElementById('tongtien');
    // let id = document.getElementById('p_id');

    fetch('/api/thanhtoan', {
        method: 'post',
        body: JSON.stringify({
            // 'tienThuoc': tienThuoc,
            'tongTien': tongTien,
            'p_id': id
        }),
        headers: {
            'Content-Type': "application/json"
        }
    }).then(function (res) {
        return res.json();

    }).then(function (data) {
        alert(data.status)
    })

}
