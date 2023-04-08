// //   fetch('/data')
// //   .then(response => response.json())
// //   .then(data => {
// //     console.log(data); // 输出获取到的数据
// //     // 将数据渲染到HTML中
// //   });

// // fetch('http://127.0.0.1:5000/data')
// //   .then(response => response.json())
// //   .then(data => console.log(data))
// //   .catch(error => console.error(error));

// // 改端口
// //   fetch('http://127.0.0.1:5000/data', {
// //     headers: {
// //         'Origin': 'http://127.0.0.1:5500/templates/index.html'
// //       }
// // // 向后台 Flask 发送 GET请求，Origin 字段设置为前端应用程序的实际地址
// //   })
// //   .then(response => response.json())
// //   .then(data => console.log(data))
// //   .catch(error => console.error(error));
// // 没改
// // fetch('http://localhost:5000/data')
// // 前端应用程序在访问后台 API 时，使用了 http://127.0.0.1:5500/data 这样的地址，而后台应用程序的端口号已经改为了5500，那么前端应用程序就无法正确访问后台 API。
// // 后台应用程序的地址为 http://localhost:5500， http://localhost:5500/data 来访问 /data 路由，而不是使用 http://127.0.0.1:5500/data。
// // fetch('http://127.0.0.1:5500/data')
// fetch('/data')
//   .then(response => response.json())
//   .then(data => {
//     console.log(data); // 输出获取到的数据
//     // 将数据渲染到HTML中
//     // document.getElementById('data-container').innerHTML = JSON.stringify(data);
//     // 找到数据容器元素
//     const dataContainer = document.getElementById('data-container');
//     // 创建一个空字符串，将用于存储表格行
//     let tableRows = '';
//     // 遍历数据数组中的每个元素
//     data.forEach(row => {
//       // 将当前行的每个值存储在单独的变量中
//       const id = row.rid;
//       const user = row['用户名称'];
//       const level = row['微博等级'];
//       const content = row['微博内容'];
//       const repost = row['微博转发量'];
//       const comment = row['微博评论量'];
//       const like = row['微博点赞'];
//       const time = row['发布时间'];
//       const keyword = row['搜索关键词'];
//       const topic = row['话题名称'];
//       const discussion = row['话题讨论数'];
//       const read = row['话题阅读数'];
//       // 将当前行的值添加到表格行中
//       tableRows += `
//         <tr>
//           <td>${id}</td>
//           <td>${user}</td>
//           <td>${level}</td>
//           <td>${content}</td>
//           <td>${repost}</td>
//           <td>${comment}</td>
//           <td>${like}</td>
//           <td>${time}</td>
//           <td>${keyword}</td>
//           <td>${topic}</td>
//           <td>${discussion}</td>
//           <td>${read}</td>
//         </tr>
//       `;
//     });
// // 将生成的行添加到表格中
//     dataContainer.innerHTML = tableRows;
//     // 数据渲染到页面中
//   })
//   .catch(error => console.error(error)); // 处理请求异常