const chartElement = document.getElementById("chart");


const chart = LightweightCharts.createChart(chartElement, {

    layout: {

        background: {
            color: "#090909"
        },

        textColor: "#ffffff"

    },


    grid: {

        vertLines: {
            color: "#222222"
        },

        horzLines: {
            color: "#222222"
        }

    },


    width: chartElement.clientWidth,

    height: 450

});



const candles = chart.addSeries(

    LightweightCharts.CandlestickSeries,

    {

        upColor: "#00ff88",

        downColor: "#ff3366",

        borderVisible: false,

        wickUpColor: "#00ff88",

        wickDownColor: "#ff3366"

    }

);



// מחיר נוכחי לשימוש בקנייה
window.currentPrice = 0;



// =========================
// GET SYMBOL FROM URL
// =========================

const parts = window.location.pathname.split("/");

const symbol = parts[2];



if(symbol){

    document.getElementById("title").innerText = symbol;


    fetch("/api/chart/" + symbol)


    .then(response => response.json())


    .then(data => {


        if(data.error){

            console.error(data.error);

            return;

        }



        const formatted = data.map(item => {


            return {


                time: item.time,


                open: Number(item.open),


                high: Number(item.high),


                low: Number(item.low),


                close: Number(item.close)


            };


        });



        candles.setData(formatted);



        chart.timeScale().fitContent();



        // מחיר אחרון

        if(formatted.length > 0){


            window.currentPrice =

            formatted[formatted.length - 1].close;



            const priceElement =

            document.getElementById("stock-price");



            if(priceElement){


                priceElement.innerText =

                "$" + window.currentPrice.toFixed(2);


            }


        }



    })


    .catch(error => {


        console.error(

            "Chart error:",

            error

        );


    });


}
