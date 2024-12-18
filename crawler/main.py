from apscheduler.schedulers.twisted import TwistedScheduler
from news_process_manager import NewsProcessManager
from stock_manager import StockManager

def main():
    scheduler = TwistedScheduler()
    news_process_manager = NewsProcessManager()
    stock_manager = StockManager()
    
    scheduler.add_job(
        stock_manager.update_stock_quotes,
        "interval",
        minutes=1,
        id="update_stock_quotes_job"
    )
    
    scheduler.add_job(
        stock_manager.upsert_forex,
        "interval",
        minutes=3,
        id="upsert_forex_job"
    )
    
    scheduler.add_job(
        stock_manager.upsert_indices,
        "interval",
        minutes=2,
        id="upsert_indices_job"    
    )
    
    scheduler.add_job(
        stock_manager.upsert_stock_info,
        "cron",  
        month="1,4,7,10",  # 1월, 4월, 7월, 10월에 실행
        day="30",  # 달 30일째
        hour="0",  # 자정 (00시)
        id="upsert_stock_info_job"
    )
    
    scheduler.add_job(
        news_process_manager.run,
        "interval",
        minutes=30,
        id="news_process_job"
    )
    
    # 크롤러 엔진 제어를 가져온다
    crawler_process = news_process_manager.get_crawler_process()
    # 스케줄러 실행
    scheduler.start()
    # 크롤러 엔진 실행
    crawler_process.start(False) 
    
if __name__ == "__main__":
    main()
