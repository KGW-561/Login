(async () => {
    const proxyUrl = "http://27.96.130.59:9990/proxy/fetch";
    // localhost 사용시 const proxyUrl = "http://localhost:9990/proxy/fetch";로 주소를 바꿔주세요
    const stockSymbolElement = document.querySelector('.symbol');
    const marketElement = document.querySelector('.current-price span:last-child');
    const companyNameElement = document.querySelector('.company-name');

    let stockSymbol = "";

    if (stockSymbolElement && marketElement) {
        stockSymbol = stockSymbolElement.textContent.trim();
        const market = marketElement.textContent.trim();
        if (market === '₩') {
            stockSymbol += '.KS';
        }
    }

    const companyName = companyNameElement.textContent;
    const apiUrl = `https://query2.finance.yahoo.com/v7/finance/chart/${stockSymbol}?interval=1wk&range=max`;

    try {
        const response = await fetch(`${proxyUrl}?url=${encodeURIComponent(apiUrl)}`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        if (!data || !data.chart || !data.chart.result) {
            throw new Error("Invalid data format");
        }

        const timestamps = data.chart.result[0].timestamp;
        const indicators = data.chart.result[0].indicators.quote[0];
        const open = indicators.open;
        const high = indicators.high;
        const low = indicators.low;
        const close = indicators.close;
        const volume = indicators.volume;

        if (!open || !high || !low || !close || !volume) {
            throw new Error("OHLC 데이터나 거래량 데이터가 누락되었습니다.");
        }

        const ohlc = timestamps.map((time, i) => [time * 1000, open[i], high[i], low[i], close[i]]);
        const volumeSeries = timestamps.map((time, i) => [time * 1000, volume[i]]);

        // 데이터 그룹화 단위 정의
        const groupingUnits = [
            ["week", [1]], // 주 단위
            ["month", [1, 2, 3, 4, 6]] // 월 단위
        ];

        // 차트 생성
        Highcharts.stockChart("stock-graph", {
            rangeSelector: {
                selected: 4
            },
            title: {
                text: `${companyName} 주식 차트`
            },
            yAxis: [
                {
                    labels: {
                        align: "right",
                        x: -3
                    },
                    title: {
                        text: "OHLC"
                    },
                    height: "60%",
                    lineWidth: 2,
                    resize: {
                        enabled: true
                    }
                },
                {
                    labels: {
                        align: "right",
                        x: -3
                    },
                    title: {
                        text: "Volume"
                    },
                    top: "65%",
                    height: "35%",
                    offset: 0,
                    lineWidth: 2
                }
            ],
            tooltip: {
                split: true
            },
            series: [
                {
                    type: "candlestick",
                    name: companyName,
                    data: ohlc,
                    dataGrouping: {
                        units: groupingUnits
                    }
                },
                {
                    type: "column",
                    name: "거래량",
                    data: volumeSeries,
                    yAxis: 1,
                    dataGrouping: {
                        units: groupingUnits
                    }
                }
            ]
        });
    } catch (error) {
        console.error("데이터 가져오기 실패:", error);
        alert("데이터를 가져오는 중 오류가 발생했습니다.");
    }
})();
