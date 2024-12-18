package com.team3.scvs.controller;

import com.team3.scvs.dto.ForexDTO;
import com.team3.scvs.dto.IndexDTO;
import com.team3.scvs.dto.KorDTO;
import com.team3.scvs.service.IndexService;
import com.team3.scvs.service.KorService;
import com.team3.scvs.service.ForexService;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.web.PageableDefault;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.PathVariable;

import java.util.List;
import java.util.stream.Collectors;

@Controller
@RequiredArgsConstructor //자동으로 생성자 생성
public class KorController {
    private final KorService korService;
    private final ForexService forexService;
    private final IndexService indexService;

    @ModelAttribute("isLoggedIn")
    public boolean setDefaultIsLoggedIn() {
        return false; //기본값 설정

    }

    //뉴스 목록 조회
    //url: /kor?page=1
    @GetMapping("/kor")
    public String getKorList(@PageableDefault(page = 1) Pageable pageable, Model model) {
        Page<KorDTO> korList = korService.getKorList(pageable); //페이징된 국내 경제 뉴스 데이터 리스트
        ForexDTO forex = forexService.getKrwUsdForex(); //환율 데이터

        //지수 데이터 필터링 (KOSPI와 KOSDAQ만)
        List<IndexDTO> indices = indexService.getIndices().stream()
                .filter(index -> "KOSPI".equals(index.getTitle()) || "KOSDAQ".equals(index.getTitle()))
                .collect(Collectors.toList());

        //페이징
        int blockLimit = 10; //한번에 보여질 페이지 번호의 개수
        int startPage = (((int)(Math.ceil((double)pageable.getPageNumber() / blockLimit))) - 1) * blockLimit + 1;
        int endPage = ((startPage + blockLimit - 1) < korList.getTotalPages()) ? startPage + blockLimit - 1 : korList.getTotalPages();

        //모델에 데이터 추가하여 뷰에 전달
        model.addAttribute("korList", korList); //뉴스 데이터 리스트
        model.addAttribute("startPage", startPage); //첫번째 페이지
        model.addAttribute("endPage", endPage); //마지막 페이지

        model.addAttribute("forex", forex); //환율 데이터
        model.addAttribute("indices", indices); //지수 데이터 (KOSPI와 KOSDAQ만)

        //뷰 템플릿
        return "News/kor";

    }

    //뉴스 상세 페이지 조회
    //url: /kor/1?page=1
    @GetMapping("/kor/{korEconNewsId}")
    public String findById(@PathVariable Long korEconNewsId, Model model,
                           @PageableDefault(page = 1) Pageable pageable) {
        KorDTO korDto = korService.findById(korEconNewsId); //korEconNewsId로 조회한 뉴스 데이터

        //모델에 데이터 추가하여 뷰에 전달
        model.addAttribute("kor", korDto); //뉴스 상세 데이터
        model.addAttribute("page", pageable.getPageNumber()); //현재 페이지

        //뷰 템플릿
        return "News/korDetail";

    }

}
