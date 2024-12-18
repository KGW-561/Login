package com.team3.scvs.controller;

import com.team3.scvs.entity.TickerEntity;
import com.team3.scvs.entity.UserWatchlistEntity;
import com.team3.scvs.entity.WatchlistStocksEntity;
import com.team3.scvs.service.WatchlistService;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;

import java.util.Comparator;
import java.util.List;

@Controller
@RequiredArgsConstructor
public class WatchlistController {

    private final WatchlistService watchlistService;

    // 관심 목록 페이지
    @GetMapping("/watchlist")
    public String viewWatchlist(@RequestParam("userId") Long userId,
                                @RequestParam(value = "watchlistId", required = false) Long watchlistId,
                                        Model model) {
        // 사용자 관심 목록 리스트 가져오기
        List<UserWatchlistEntity> watchlists = watchlistService.getUserWatchlists(userId);

        // 관심 목록에 있는 종목 리스트 추출하기
        List<WatchlistStocksEntity> watchlistStocks = watchlists.stream()
                .flatMap(watchlist -> watchlist.getStocks().stream()) //리스트안에 리스트를 하나의 스트림으로 평탄화 작업
                .sorted(Comparator.comparing(stock -> stock.getTicker().getSymbol()))  // Symbol 기준으로 정렬
                .toList();

        // 전체 종목 리스트 가져오기
        List<TickerEntity> allTickers = watchlistService.getAllTickers();

        // 모델에 관심 목록 리스트와 전체 종목 리스트 추가
        model.addAttribute("watchlistStocks", watchlistStocks);
        model.addAttribute("allTickers", allTickers);
        model.addAttribute("userId", userId);
        model.addAttribute("watchlistId", watchlistId);
        // 로그인 구현되면 삭제
        model.addAttribute("isLoggedIn", true);

        return "Stockwatch/watchlist";
    }



    // 관심 목록에 종목 추가
    @PostMapping("/watchlist/add")
    public String addToWatchlist(@RequestParam("userId") Long userId,
                                 @RequestParam("tickerId") Long tickerId) {
        try {
            // 관심 목록이 있는지 확인하고 없으면 새로 생성
            UserWatchlistEntity watchlist = watchlistService.getOrCreateWatchlist(userId);

            // 지정된 관심 목록에 종목 추가
            watchlistService.addStockToWatchlist(watchlist.getUserWatchlistId(), tickerId);

            // 관심 목록 페이지로 리다이렉트
            return "redirect:/watchlist?userId=" + userId;
        } catch (Exception e) {
            // 500 에러 발생 시 관심 목록 페이지로 리다이렉트
            return "redirect:/watchlist?userId=" + userId;
        }
    }


    // 관심 목록에서 종목 삭제
    @PostMapping("/watchlist/delete")
    public String deleteStockFromWatchlist(@RequestParam("watchlistId") Long watchlistId,
                                           @RequestParam("tickerId") Long tickerId,
                                           @RequestParam("userId") Long userId) {
        // 관심 목록에서 특정 종목 삭제
        watchlistService.deleteStockFromWatchlist(watchlistId, tickerId);

        // 관심 목록 페이지로 리다이렉트
        return "redirect:/watchlist?userId=" + userId;
    }

}
