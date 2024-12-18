package com.team3.scvs.controller;

import com.team3.scvs.dto.*;

import com.team3.scvs.service.StocksService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.web.PageableDefault;
import org.springframework.stereotype.Controller;

import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestParam;

import java.util.Optional;


@Controller
public class StockWatchController {

    @Autowired
    private StocksService stocksService;

    @GetMapping("/stockwatch")
    public String stockwatch(@RequestParam("tickerId") Long tickerId,
                             @PageableDefault(page = 1) Pageable pageable,
                             Model model) {
        // 주식 정보 가져오기
        CommunityStockInfoDTO stockInfo = stocksService.getStockInfo(tickerId);

        //뉴스 정보 가져오기
        Page<StockNewsDTO> stockNews = stocksService.getStockNewsList(tickerId,pageable);

        //페이징
        int blockLimit = 10; //한번에 보여질 페이지 번호의 개수
        int startPage = (((int)(Math.ceil((double)pageable.getPageNumber() / blockLimit))) - 1) * blockLimit + 1;
        int endPage = ((startPage + blockLimit - 1) < stockNews.getTotalPages()) ? startPage + blockLimit - 1 : stockNews.getTotalPages();

        // 마켓 정보 가져오기
        Optional<StocksDTO> stockinfoOptional = stocksService.getStocksInfo(tickerId);
        StocksDTO marketinfo = stockinfoOptional.orElse(null);

        // 최신 댓글 정보 가져오기
        CommunityDTO community = stocksService.getOrCreateCommunity(tickerId);
        long communityId = community.getCommunityId();

        CommunityCommentViewDTO latestComment = stocksService.getLatestComment(communityId);
        long totalComments = stocksService.getTotalComments(communityId);

        // 로그인 구현되면 삭제
        model.addAttribute("isLoggedIn", true);
        model.addAttribute("stockInfo", stockInfo);
        model.addAttribute("marketinfo", marketinfo);
        model.addAttribute("latestComment", latestComment);
        model.addAttribute("totalComments", totalComments);
        model.addAttribute("tickerId", tickerId);
        model.addAttribute("stockNews", stockNews);
        model.addAttribute("startPage", startPage); //첫번째 페이지
        model.addAttribute("endPage", endPage); //마지막 페이지
        return "Stockwatch/stockwatch"; // 경로는 templates 폴더 내 위치 기준
    }

    //주식 뉴스 상세 페이지 조회
    //url: /stocknews/1/1?page=1
    @GetMapping("/stocknews/{tickerId}/{stockNewsId}")
    public String findById(@PathVariable Long tickerId,
                           @PathVariable String stockNewsId,
                           Model model,
                           @PageableDefault(page = 1) Pageable pageable) {
        StockNewsDTO stockNewsDTO = stocksService.findById(stockNewsId, tickerId); //vm_stock_news에서 stockNewsId와 tickerId로 데이터 조회

        if (stockNewsDTO == null) {//뉴스 데이터가 없는 경우
            model.addAttribute("errorMessage", "뉴스 데이터를 찾을 수 없습니다.");

            //에러 페이지로 이동
            return "Error/404";

        }

        //모델에 데이터 추가하여 뷰에 전달
        model.addAttribute("stocknews", stockNewsDTO); //뉴스 상세 데이터
        model.addAttribute("tickerId", tickerId); //종목 티커 아이디 데이터
        model.addAttribute("page", pageable.getPageNumber()); //현재 페이지

        //뷰 템플릿
        return "News/stocknews";

    }

}
