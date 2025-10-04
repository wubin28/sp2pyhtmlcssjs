/*
JavaScript交互脚本 - JavaScript学习示例

学习要点：
1. 异步操作（async/await、fetch API）
2. JSON数据解析
3. DOM操作（获取元素、修改内容）
4. Chart.js图表库使用
5. 数据处理和转换
*/

// ============================================================
// 主函数：加载数据并初始化看板
// ============================================================
// async关键字：表示这是一个异步函数，可以使用await
async function initDashboard() {
    try {
        // 第一步：加载JSON数据
        console.log('正在加载数据...');  // console.log()：在浏览器控制台输出信息

        // fetch()：浏览器内置的网络请求API，用于获取资源
        // await关键字：等待异步操作完成
        const response = await fetch('results.json');

        // 检查请求是否成功
        if (!response.ok) {
            throw new Error('数据加载失败');  // throw：抛出错误
        }

        // response.json()：将响应体解析为JSON对象
        const data = await response.json();
        console.log('数据加载成功:', data);

        // 第二步：更新统计数字
        updateStats(data);

        // 第三步：创建三个图表
        createChart1(data.question1);
        createChart2(data.question2);
        createChart3(data.question3);

    } catch (error) {
        // catch：捕获错误并处理
        console.error('错误:', error);  // console.error()：输出错误信息
        alert('数据加载失败，请确保已运行 analyze_data.py 生成 results.json 文件');
    }
}

// ============================================================
// 更新统计数字
// ============================================================
function updateStats(data) {
    // DOM操作：通过ID获取HTML元素
    // document.getElementById()：根据id属性查找元素
    const totalRecordsElement = document.getElementById('total-records');
    const multimodalCountElement = document.getElementById('multimodal-count');

    // 修改元素的文本内容
    // textContent属性：设置或获取元素的纯文本内容
    totalRecordsElement.textContent = data.total_records;

    // 计算总的multimodal数量
    // reduce()：数组方法，累加所有项的值
    const totalMultimodal = data.question1.data.reduce((sum, item) => {
        return sum + item.multimodal_count;  // sum是累加器，item是当前项
    }, 0);  // 0是初始值

    multimodalCountElement.textContent = totalMultimodal;
}

// ============================================================
// 创建图表1：Agent Types
// ============================================================
function createChart1(questionData) {
    // 获取canvas元素
    const ctx = document.getElementById('chart-question1').getContext('2d');

    // 从数据中提取标签和值
    // map()：数组方法，将每个元素转换为新值
    const labels = questionData.data.map(item => item.name);
    const ratios = questionData.data.map(item => item.ratio * 100);  // 转换为百分比

    // 创建Chart.js图表
    // new Chart()：Chart.js的构造函数
    new Chart(ctx, {
        type: 'bar',  // 图表类型：柱状图
        data: {
            labels: labels,  // X轴标签
            datasets: [{
                label: 'Multimodal比例 (%)',  // 数据集标签
                data: ratios,  // Y轴数据
                backgroundColor: [  // 柱子颜色（渐变）
                    'rgba(74, 144, 226, 0.7)',
                    'rgba(122, 184, 245, 0.7)',
                    'rgba(107, 207, 126, 0.7)'
                ],
                borderColor: [  // 边框颜色
                    'rgba(74, 144, 226, 1)',
                    'rgba(122, 184, 245, 1)',
                    'rgba(107, 207, 126, 1)'
                ],
                borderWidth: 2  // 边框宽度
            }]
        },
        options: {
            responsive: true,  // 响应式：自动适应容器大小
            maintainAspectRatio: false,  // 不保持宽高比，使用容器高度
            plugins: {
                legend: {
                    display: true,  // 显示图例
                    position: 'top'
                },
                title: {
                    display: true,
                    text: questionData.title
                }
            },
            scales: {
                y: {
                    beginAtZero: true,  // Y轴从0开始
                    title: {
                        display: true,
                        text: '比例 (%)'
                    }
                }
            }
        }
    });
}

// ============================================================
// 创建图表2：Model Architectures
// ============================================================
function createChart2(questionData) {
    const ctx = document.getElementById('chart-question2').getContext('2d');

    const labels = questionData.data.map(item => item.name);
    const ratios = questionData.data.map(item => item.ratio * 100);

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Multimodal比例 (%)',
                data: ratios,
                backgroundColor: [
                    'rgba(255, 159, 64, 0.7)',
                    'rgba(255, 205, 86, 0.7)',
                    'rgba(153, 102, 255, 0.7)'
                ],
                borderColor: [
                    'rgba(255, 159, 64, 1)',
                    'rgba(255, 205, 86, 1)',
                    'rgba(153, 102, 255, 1)'
                ],
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    position: 'top'
                },
                title: {
                    display: true,
                    text: questionData.title
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: '比例 (%)'
                    }
                }
            }
        }
    });
}

// ============================================================
// 创建图表3：Task Categories
// ============================================================
function createChart3(questionData) {
    const ctx = document.getElementById('chart-question3').getContext('2d');

    const labels = questionData.data.map(item => item.name);
    const scores = questionData.data.map(item => item.median_score);

    // 这次使用横向柱状图（horizontalBar效果）
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Median Bias Detection Score',
                data: scores,
                backgroundColor: [
                    'rgba(54, 162, 235, 0.7)',
                    'rgba(75, 192, 192, 0.7)',
                    'rgba(201, 203, 207, 0.7)'
                ],
                borderColor: [
                    'rgba(54, 162, 235, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(201, 203, 207, 1)'
                ],
                borderWidth: 2
            }]
        },
        options: {
            indexAxis: 'y',  // 设置为'y'使柱状图横向显示
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    position: 'top'
                },
                title: {
                    display: true,
                    text: questionData.title
                }
            },
            scales: {
                x: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Bias Detection Score'
                    }
                }
            }
        }
    });
}

// ============================================================
// 页面加载完成后自动执行
// ============================================================
// DOMContentLoaded事件：当HTML文档完全加载和解析后触发
// addEventListener()：添加事件监听器
document.addEventListener('DOMContentLoaded', function() {
    console.log('页面加载完成，开始初始化看板...');
    initDashboard();  // 调用主函数
});
