package com.team3.scvs.service;

import com.team3.scvs.dto.IndexDTO;
import com.team3.scvs.repository.IndexRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
public class IndexService {

    @Autowired
    private IndexRepository indexRepository;

    public List<IndexDTO> getIndices(){
        return indexRepository.findAll().stream()
                .map(index -> new IndexDTO(
                        index.getTitle(),
                        index.getCurrentValue(),
                        index.getChangeValue(),
                        index.getChangePercent()))
                .collect(Collectors.toList());
    }
}
