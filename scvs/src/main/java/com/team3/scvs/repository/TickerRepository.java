package com.team3.scvs.repository;

import com.team3.scvs.entity.TickerEntity;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;


public interface TickerRepository extends JpaRepository<TickerEntity, Long> {
}
