import { TestBed } from '@angular/core/testing';

import { ApigatewayService } from './apigateway.service';

describe('ApigatewayService', () => {
  let service: ApigatewayService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(ApigatewayService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
