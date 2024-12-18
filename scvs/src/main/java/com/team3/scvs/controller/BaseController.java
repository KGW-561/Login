package com.team3.scvs.controller;

import com.team3.scvs.dto.ForexDTO;
import com.team3.scvs.dto.IndexDTO;
import com.team3.scvs.dto.KorDTO;
import com.team3.scvs.dto.UsaDTO;
import com.team3.scvs.service.ForexService;
import com.team3.scvs.service.IndexService;
import com.team3.scvs.service.KorService;
import com.team3.scvs.service.UsaService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.ModelAttribute;

import java.util.List;

@Controller
public class BaseController {

    @Autowired
    private IndexService indexService;

    @Autowired
    private ForexService forexService;

    @Autowired
    private KorService korService;

    @Autowired
    private UsaService usaService;

    @ModelAttribute("isLoggedIn") // 자동으로 설정
    public boolean setDefaultIsLoggedIn() {
        return false; // 기본값 설정
    }

    @GetMapping("/")
    public String mainPage(Model model) {
        List<IndexDTO> indices = indexService.getIndices();
        ForexDTO krwUsdForex = forexService.getKrwUsdForex();

        List<KorDTO> korNews = korService.getMainHomeNews();
        List<UsaDTO> usaNews = usaService.getMainHomeNews();

        model.addAttribute("usaNews", usaNews);
        model.addAttribute("korNews", korNews);
        model.addAttribute("indices", indices);
        model.addAttribute("forex", krwUsdForex);
        return "index";
    }
}
