// $(document).ready(function () {
//
//
//
//     $('#ololo').on("click", function () {
//         console.log('run!')
//         $.ajax({
//             url: "/login",
//             type: "POST",
//             contentType: "application/json",
//             data: {},
//             headers: {
//                 "Authorization": "Basic xxxxx"
//             },
//             success: function (request) {
//                 alert('okey, 1');
//                 return false;
//             },
//             error: function (jqXHR, textStatus, errorThrown) {
//                 alert('not okey, 1');
//                 console.log('[error]');
//                 console.log(jqXHR);
//                 console.log(textStatus);
//                 console.log(errorThrown);
//                 return false;
//             },
//             dataType: "json"
//         })
//     })
// });
//
// //     $('#btn_login').on("click", function () {
// //         document.location.reload();
// //         return false;
// //     });
// //
// //     $('#btn_restore').on("click", function () {
// //         document.location.href = '/restore';
// //         return false;
// //     });
// //
// //     $('#btn_register').on("click", function () {
// //         document.location.href = '/register';
// //         return false;
// //     });
// // })
// // ;